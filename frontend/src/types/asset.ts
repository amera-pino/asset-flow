// 備品一覧・申請画面で表示する在庫計算済みの備品データ
export type Asset = {
  id: number;
  name: string;
  category: string;
  total_stock: number;
  consuming_quantity: number;
  effective_stock: number;
  status: string;
  created_at: string;
  updated_at: string;
};
