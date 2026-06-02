import { CalendarDays, PackageCheck, RotateCcw, UserRound } from "lucide-react";
import { Link } from "react-router-dom";

type MockActiveRequest = {
  id: number;
  assetName: string;
  category: string;
  quantity: number;
  requesterName: string;
  userId: number;
  startDate: string;
  endDate: string;
  status: "貸出中";
};

const MOCK_ACTIVE_REQUESTS: MockActiveRequest[] = [
  {
    id: 101,
    assetName: "ノートPC ThinkPad X1",
    category: "PC",
    quantity: 1,
    requesterName: "固定ユーザー",
    userId: 1,
    startDate: "2026-06-01",
    endDate: "2026-06-07",
    status: "貸出中",
  },
  {
    id: 102,
    assetName: "Web会議用マイクスピーカー",
    category: "会議機材",
    quantity: 1,
    requesterName: "固定ユーザー",
    userId: 1,
    startDate: "2026-06-02",
    endDate: "2026-06-05",
    status: "貸出中",
  },
];

export function MyRequestsPage() {
  const activeRequests = MOCK_ACTIVE_REQUESTS.filter((request) => request.userId === 1 && request.status === "貸出中");

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

        {activeRequests.length === 0 ? (
          <section className="rounded-md border border-dashed border-slate-300 bg-white px-6 py-12 text-center shadow-sm">
            <div className="mx-auto flex size-12 items-center justify-center rounded-md bg-slate-100 text-slate-500">
              <PackageCheck className="size-6" />
            </div>
            <p className="mt-4 text-sm font-medium text-slate-700">現在、あなたが借りている備品はありません。</p>
          </section>
        ) : (
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
                        <h3 className="text-base font-semibold text-slate-950">{request.assetName}</h3>
                        <span className="inline-flex rounded-md bg-teal-50 px-2 py-1 text-xs font-medium text-teal-700">
                          {request.status}
                        </span>
                      </div>
                      <p className="mt-1 text-sm text-slate-600">
                        {request.category} / 数量 {request.quantity}
                      </p>

                      <dl className="mt-4 grid gap-3 text-sm sm:grid-cols-2">
                        <div className="flex items-center gap-2 text-slate-600">
                          <CalendarDays className="size-4 text-slate-400" />
                          <span>
                            {request.startDate} - {request.endDate}
                          </span>
                        </div>
                        <div className="flex items-center gap-2 text-slate-600">
                          <UserRound className="size-4 text-slate-400" />
                          <span>{request.requesterName}</span>
                        </div>
                      </dl>
                    </div>
                  </div>

                  <button
                    className="inline-flex h-10 w-full items-center justify-center gap-2 rounded-md bg-teal-700 px-4 text-sm font-medium text-white shadow-sm transition hover:bg-teal-800 focus:outline-none focus:ring-2 focus:ring-teal-200 md:w-32"
                    type="button"
                  >
                    <RotateCcw className="size-4" />
                    返却する
                  </button>
                </article>
              ))}
            </div>
          </section>
        )}
      </div>
    </main>
  );
}
