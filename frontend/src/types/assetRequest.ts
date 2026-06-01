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
  status: "pending" | "approved" | "rejected" | "cancelled";
  created_at: string;
  updated_at: string;
};
