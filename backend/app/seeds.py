from datetime import datetime, timedelta, timezone

from app.core.database import SessionLocal, create_tables
from app.models.asset import Asset


BASE_CREATED_AT = datetime(2026, 6, 1, 11, 35, tzinfo=timezone.utc)


SEED_ASSET_DATA = [
    {
        "name": 'MacBook Pro 14"',
        "category": "パソコン",
        "total_stock": 3,
        "status": "available",
    },
    {
        "name": 'Dell 27" 4K Monitor',
        "category": "モニター",
        "total_stock": 5,
        "status": "available",
    },
    {
        "name": "HHKB Studio",
        "category": "キーボード",
        "total_stock": 2,
        "status": "available",
    },
    {
        "name": "Magic Mouse",
        "category": "マウス",
        "total_stock": 10,
        "status": "available",
    },
    {
        "name": "Herman Miller Aeron",
        "category": "家具",
        "total_stock": 2,
        "status": "available",
    },
    {
        "name": "Jabra Speak2 75",
        "category": "会議機器",
        "total_stock": 4,
        "status": "available",
    },
    {
        "name": "Sony WH-1000XM5",
        "category": "ヘッドセット",
        "total_stock": 6,
        "status": "available",
    },
    {
        "name": "Anker 737 Power Bank",
        "category": "アクセサリー",
        "total_stock": 8,
        "status": "available",
    },
    {"name": "Apple MacBook Air 13", "category": "パソコン", "total_stock": 7, "status": "available"},
    {"name": "ThinkPad X1 Carbon", "category": "パソコン", "total_stock": 4, "status": "available"},
    {"name": "Surface Laptop 6", "category": "パソコン", "total_stock": 5, "status": "available"},
    {"name": "HP EliteBook 840", "category": "パソコン", "total_stock": 6, "status": "available"},
    {"name": "ASUS Zenbook 14", "category": "パソコン", "total_stock": 3, "status": "available"},
    {"name": "4K Display 32", "category": "モニター", "total_stock": 8, "status": "available"},
    {"name": "2K Portable Monitor", "category": "モニター", "total_stock": 5, "status": "available"},
    {"name": "液晶ディスプレイ 24インチ", "category": "モニター", "total_stock": 9, "status": "available"},
    {"name": "BenQ ScreenBar Halo", "category": "周辺機器", "total_stock": 4, "status": "available"},
    {"name": "モニターアーム シングル", "category": "周辺機器", "total_stock": 11, "status": "available"},
    {"name": "Logitech MX Keys", "category": "キーボード", "total_stock": 6, "status": "available"},
    {"name": "Keychron K3 Pro", "category": "キーボード", "total_stock": 5, "status": "available"},
    {"name": "日本語配列キーボード", "category": "キーボード", "total_stock": 7, "status": "available"},
    {"name": "テンキー付きキーボード", "category": "キーボード", "total_stock": 3, "status": "available"},
    {"name": "Logitech MX Master 3S", "category": "マウス", "total_stock": 8, "status": "available"},
    {"name": "USB-C Travel Mouse", "category": "マウス", "total_stock": 12, "status": "available"},
    {"name": "静音ワイヤレスマウス", "category": "マウス", "total_stock": 10, "status": "available"},
    {"name": "Webカメラ 1080p", "category": "カメラ", "total_stock": 6, "status": "available"},
    {"name": "Logitech Brio 4K", "category": "カメラ", "total_stock": 4, "status": "available"},
    {"name": "360 Meeting Camera", "category": "会議機器", "total_stock": 2, "status": "available"},
    {"name": "Poly Studio P15", "category": "会議機器", "total_stock": 3, "status": "available"},
    {"name": "会議用スピーカーフォン", "category": "会議機器", "total_stock": 5, "status": "available"},
    {"name": "Yamaha YVC-200", "category": "会議機器", "total_stock": 4, "status": "available"},
    {"name": "AirPods Pro 2", "category": "ヘッドセット", "total_stock": 6, "status": "available"},
    {"name": "Bose QuietComfort", "category": "ヘッドセット", "total_stock": 3, "status": "available"},
    {"name": "有線ヘッドセット", "category": "ヘッドセット", "total_stock": 8, "status": "available"},
    {"name": "ノイズキャンセルヘッドホン", "category": "ヘッドセット", "total_stock": 4, "status": "available"},
    {"name": "USB-C Hub 7-in-1", "category": "アクセサリー", "total_stock": 15, "status": "available"},
    {"name": "HDMI Adapter", "category": "アクセサリー", "total_stock": 18, "status": "available"},
    {"name": "65W USB-C Charger", "category": "電源機器", "total_stock": 12, "status": "available"},
    {"name": "100W GaN Charger", "category": "電源機器", "total_stock": 7, "status": "available"},
    {"name": "延長電源タップ", "category": "電源機器", "total_stock": 9, "status": "available"},
    {"name": "iPad Pro 11", "category": "タブレット", "total_stock": 4, "status": "available"},
    {"name": "iPad Air", "category": "タブレット", "total_stock": 5, "status": "available"},
    {"name": "Android Tablet 10", "category": "タブレット", "total_stock": 3, "status": "available"},
    {"name": "タブレットスタンド", "category": "アクセサリー", "total_stock": 8, "status": "available"},
    {"name": "1TB Portable SSD", "category": "ストレージ", "total_stock": 6, "status": "available"},
    {"name": "2TB Backup HDD", "category": "ストレージ", "total_stock": 5, "status": "available"},
    {"name": "外付けSSD 500GB", "category": "ストレージ", "total_stock": 7, "status": "available"},
    {"name": "Wi-Fi 6 Router", "category": "ネットワーク", "total_stock": 3, "status": "available"},
    {"name": "8-Port Gigabit Switch", "category": "ネットワーク", "total_stock": 4, "status": "available"},
    {"name": "LANケーブル 5m", "category": "ネットワーク", "total_stock": 20, "status": "available"},
    {"name": "Ergonomic Chair", "category": "家具", "total_stock": 5, "status": "available"},
    {"name": "昇降デスク", "category": "家具", "total_stock": 3, "status": "available"},
    {"name": "フットレスト", "category": "家具", "total_stock": 6, "status": "available"},
    {"name": "卓上マイク", "category": "オーディオ", "total_stock": 4, "status": "available"},
    {"name": "Blue Yeti Microphone", "category": "オーディオ", "total_stock": 2, "status": "available"},
]


SEED_ASSETS = [
    {
        **asset_data,
        "created_at": BASE_CREATED_AT - timedelta(minutes=index * 37),
        "updated_at": BASE_CREATED_AT - timedelta(minutes=index * 37),
    }
    for index, asset_data in enumerate(SEED_ASSET_DATA)
]


def seed_assets() -> None:
    create_tables()

    db = SessionLocal()
    try:
        created_count = 0
        updated_count = 0

        for asset_data in SEED_ASSETS:
            asset = db.query(Asset).filter(Asset.name == asset_data["name"]).one_or_none()

            if asset is None:
                db.add(Asset(**asset_data))
                created_count += 1
                continue

            asset.category = asset_data["category"]
            asset.total_stock = asset_data["total_stock"]
            asset.status = asset_data["status"]
            asset.created_at = asset_data["created_at"]
            asset.updated_at = asset_data["updated_at"]
            updated_count += 1

        db.commit()
        print(f"Seed completed: created={created_count}, updated={updated_count}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_assets()
