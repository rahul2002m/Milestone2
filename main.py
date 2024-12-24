from aggregator.data_aggregator import run
import traceback


if __name__ == "__main__":
    product_map = {
        "amazon": [
            ""
        ],
        "flipkart": [
            ""
        ]
    }

    try:
        final_data = aggregator.run(product_map)
        print("Final Aggregated Data:", final_data)
    except:
        traceback.print_exc()
