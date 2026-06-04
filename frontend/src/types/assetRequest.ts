export type AssetRequestCreate = {
  asset_id: number;
  requester_name: string;
  start_date: string;
  end_date: string;
  reason: string;
  quantity: number;
};

export type AssetRequest = AssetRequestCreate & {
  id: number;
  user_id: number;
  status: "pending" | "loaned" | "returned" | "cancelled";
  returned_at: string | null;
  created_at: string;
  updated_at: string;
};

export type ActiveAssetRequest = AssetRequest & {
  asset_name: string;
  asset_category: string;
};
