import random
import pandas as pd


def generate_ads_data(num_rows=1000):
    data = []

    for _ in range(num_rows):
        cost = random.randint(10, 100)
        priority = random.choice([1, 2, 3])

        # clicks influenced by cost & priority
        clicks = random.randint(20, 200) + (priority * 10)

        # conversion rate (1% to 10%)
        conversion_rate = random.uniform(0.01, 0.10)
        conversions = int(clicks * conversion_rate)

        # revenue influenced by conversions
        revenue = conversions * random.randint(20, 60)

        value_score = round(revenue / cost, 2)

        data.append({
            "cost": cost,
            "priority": priority,
            "clicks": clicks,
            "conversions": conversions,
            "revenue": revenue,
            "value_score": value_score
        })

    return pd.DataFrame(data)


if __name__ == "__main__":
    df = generate_ads_data(1000)
    df.to_csv("data/raw/ads_historical.csv", index=False)
    print("Synthetic ads data generated.")
