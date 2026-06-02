import { CalendarDays, PackageCheck, RotateCcw, UserRound } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { ApiClientError, apiFetch } from "../lib/api";
import type { ActiveAssetRequest, AssetRequest } from "../types/assetRequest";

export function MyRequestsPage() {
  const [activeRequests, setActiveRequests] = useState<ActiveAssetRequest[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [returningRequestId, setReturningRequestId] = useState<number | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [isToastVisible, setIsToastVisible] = useState(false);

  const fetchActiveRequests = useCallback(async (signal?: AbortSignal) => {
    const data = await apiFetch<ActiveAssetRequest[]>("/api/requests/me/active", { signal });
    setActiveRequests(data);
  }, []);

  useEffect(() => {
    const abortController = new AbortController();

    async function loadActiveRequests() {
      setIsLoading(true);
      setErrorMessage(null);

      try {
        await fetchActiveRequests(abortController.signal);
      } catch (error) {
        if (abortController.signal.aborted) {
          return;
        }

        setErrorMessage(error instanceof ApiClientError ? error.message : "貸出状況の取得に失敗しました。");
      } finally {
        if (!abortController.signal.aborted) {
          setIsLoading(false);
        }
      }
    }

    void loadActiveRequests();

    return () => {
      abortController.abort();
    };
  }, [fetchActiveRequests]);

  useEffect(() => {
    if (!toastMessage) {
      return;
    }

    setIsToastVisible(false);
    const showTimeoutId = window.setTimeout(() => {
      setIsToastVisible(true);
    }, 10);
    const timeoutId = window.setTimeout(() => {
      setIsToastVisible(false);
      setToastMessage(null);
    }, 3000);

    return () => {
      window.clearTimeout(showTimeoutId);
      window.clearTimeout(timeoutId);
    };
  }, [toastMessage]);

  async function handleReturn(request: ActiveAssetRequest) {
    if (returningRequestId !== null) {
      return;
    }

    setReturningRequestId(request.id);
    setErrorMessage(null);

    try {
      await apiFetch<AssetRequest>(`/api/requests/${request.id}/return`, {
        method: "POST",
      });
      await fetchActiveRequests();
      setToastMessage(`${request.asset_name} を返却しました。`);
    } catch (error) {
      setErrorMessage(error instanceof ApiClientError ? error.message : "返却処理に失敗しました。");
    } finally {
      setReturningRequestId(null);
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 text-slate-950">
      <div className="mx-auto flex w-full max-w-5xl flex-col gap-6 px-6 py-8">
        <header className="flex flex-col gap-4 border-b border-slate-200 pb-6 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm font-medium text-teal-700">AssetFlow</p>
            <h1 className="mt-1 text-3xl font-semibold tracking-normal text-slate-950">マイ貸出状況</h1>
          </div>

          <nav aria-label="メインナビゲーション" className="flex flex-wrap gap-2">
            <Link
              className="inline-flex h-10 items-center justify-center rounded-md border border-slate-300 bg-white px-4 text-sm font-medium text-slate-700 transition hover:bg-slate-100"
              to="/"
            >
              備品一覧
            </Link>
            <Link
              aria-current="page"
              className="inline-flex h-10 items-center justify-center rounded-md bg-teal-700 px-4 text-sm font-medium text-white shadow-sm"
              to="/my-requests"
            >
              マイ貸出状況
            </Link>
          </nav>
        </header>

        {toastMessage ? (
          <div
            className={`fixed left-1/2 top-0 z-50 -translate-x-1/2 rounded-b-md border border-t-0 border-teal-200 bg-teal-50 px-5 py-3 text-sm font-medium text-teal-800 shadow-md transition-transform duration-300 ${
              isToastVisible ? "translate-y-0" : "-translate-y-full"
            }`}
          >
            {toastMessage}
          </div>
        ) : null}

        <section className="grid gap-4 sm:grid-cols-3">
          <div className="rounded-md border border-slate-200 bg-white px-4 py-3">
            <p className="text-xs text-slate-500">ログインユーザー</p>
            <p className="mt-1 text-lg font-semibold text-slate-950">user_id = 1</p>
          </div>
          <div className="rounded-md border border-slate-200 bg-white px-4 py-3">
            <p className="text-xs text-slate-500">現在貸出中</p>
            <p className="mt-1 text-lg font-semibold text-slate-950">{activeRequests.length}</p>
          </div>
          <div className="rounded-md border border-slate-200 bg-white px-4 py-3">
            <p className="text-xs text-slate-500">返却待ち数量</p>
            <p className="mt-1 text-lg font-semibold text-slate-950">
              {activeRequests.reduce((total, request) => total + request.quantity, 0)}
            </p>
          </div>
        </section>

        {errorMessage ? (
          <div className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {errorMessage}
          </div>
        ) : null}

        {isLoading ? (
          <div className="rounded-md border border-slate-200 bg-white px-5 py-4 text-sm text-slate-500">
            貸出状況を読み込み中...
          </div>
        ) : null}

        {!isLoading && activeRequests.length === 0 ? (
          <section className="rounded-md border border-dashed border-slate-300 bg-white px-6 py-12 text-center shadow-sm">
            <div className="mx-auto flex size-12 items-center justify-center rounded-md bg-slate-100 text-slate-500">
              <PackageCheck className="size-6" />
            </div>
            <p className="mt-4 text-sm font-medium text-slate-700">現在、あなたが借りている備品はありません。</p>
          </section>
        ) : null}

        {!isLoading && activeRequests.length > 0 ? (
          <section className="overflow-hidden rounded-md border border-slate-200 bg-white shadow-sm">
            <div className="border-b border-slate-200 px-5 py-4">
              <h2 className="text-base font-semibold text-slate-950">貸出中の備品</h2>
            </div>

            <div className="divide-y divide-slate-200">
              {activeRequests.map((request) => (
                <article className="grid gap-4 px-5 py-5 md:grid-cols-[minmax(0,1fr)_auto] md:items-center" key={request.id}>
                  <div className="flex gap-4">
                    <div className="flex size-11 shrink-0 items-center justify-center rounded-md bg-teal-50 text-teal-700">
                      <PackageCheck className="size-5" />
                    </div>

                    <div className="min-w-0">
                      <div className="flex flex-wrap items-center gap-2">
                        <h3 className="text-base font-semibold text-slate-950">{request.asset_name}</h3>
                        <span className="inline-flex rounded-md bg-teal-50 px-2 py-1 text-xs font-medium text-teal-700">
                          {request.status}
                        </span>
                      </div>
                      <p className="mt-1 text-sm text-slate-600">
                        {request.asset_category} / 数量 {request.quantity}
                      </p>

                      <dl className="mt-4 grid gap-3 text-sm sm:grid-cols-2">
                        <div className="flex items-center gap-2 text-slate-600">
                          <CalendarDays className="size-4 text-slate-400" />
                          <span>
                            {request.start_date} - {request.end_date}
                          </span>
                        </div>
                        <div className="flex items-center gap-2 text-slate-600">
                          <UserRound className="size-4 text-slate-400" />
                          <span>{request.requester_name}</span>
                        </div>
                      </dl>
                    </div>
                  </div>

                  <button
                    className="inline-flex h-10 w-full items-center justify-center gap-2 rounded-md bg-teal-700 px-4 text-sm font-medium text-white shadow-sm transition hover:bg-teal-800 focus:outline-none focus:ring-2 focus:ring-teal-200 disabled:cursor-not-allowed disabled:bg-slate-300 md:w-32"
                    disabled={returningRequestId !== null}
                    onClick={() => void handleReturn(request)}
                    type="button"
                  >
                    <RotateCcw className="size-4" />
                    {returningRequestId === request.id ? "返却中..." : "返却する"}
                  </button>
                </article>
              ))}
            </div>
          </section>
        ) : null}
      </div>
    </main>
  );
}
