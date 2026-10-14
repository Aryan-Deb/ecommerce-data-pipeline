import argparse
import pandas as pd

from validate import (
    validate_customers,
    validate_products,
    validate_orders,
    validate_order_items,
    print_validation_report,
)

from transform import (
    transform_customers,
    transform_products,
    transform_orders,
    transform_order_items,
    print_transformation_summary,
)

from load import (
    load_data,
    incremental_load_data,
    upsert_data,
)

from analytics import run_analytics

from run_tracker import (
    start_pipeline_run,
    complete_pipeline_run,
    fail_pipeline_run,
)

from logger import get_logger
from config import RAW_DATA_DIR, PROCESSED_DATA_DIR


logger = get_logger()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="E-commerce Data Engineering ETL Pipeline"
    )

    mode_group = parser.add_mutually_exclusive_group()

    mode_group.add_argument(
        "--incremental",
        action="store_true",
        help="Load only new records into PostgreSQL",
    )

    mode_group.add_argument(
        "--upsert",
        action="store_true",
        help="Insert new records and update existing records",
    )

    return parser.parse_args()


def main(args):

    print("\n")
    print("=" * 40)
    print("      E-COMMERCE ETL PIPELINE")
    print("=" * 40)

    run_id = None

    try:

        # --------------------------------------------------
        # 1. START PIPELINE RUN
        # --------------------------------------------------

        run_id = start_pipeline_run()

        logger.info(
            f"Pipeline run started | run_id={run_id}"
        )

        # --------------------------------------------------
        # 2. LOAD RAW DATA
        # --------------------------------------------------

        print("\nLoading raw data...")

        logger.info("Loading raw data")

        customers = pd.read_csv(
            f"{RAW_DATA_DIR}/customers.csv"
        )

        products = pd.read_csv(
            f"{RAW_DATA_DIR}/products.csv"
        )

        orders = pd.read_csv(
            f"{RAW_DATA_DIR}/orders.csv"
        )

        order_items = pd.read_csv(
            f"{RAW_DATA_DIR}/order_items.csv"
        )

        print("Raw data loaded successfully.")

        logger.info(
            "Raw data loaded successfully"
        )

        # --------------------------------------------------
        # 3. DATA VALIDATION
        # --------------------------------------------------

        print("\nRunning data validation...")

        logger.info(
            "Starting data validation"
        )

        validation_reports = [
            validate_customers(customers),
            validate_products(products),
            validate_orders(orders),
            validate_order_items(order_items),
        ]

        print_validation_report(
            validation_reports
        )

        logger.info(
            "Data validation completed"
        )

        # --------------------------------------------------
        # 4. DATA TRANSFORMATION
        # --------------------------------------------------

        print("\nTransforming data...")

        logger.info(
            "Starting data transformation"
        )

        # Clean customers
        customers_clean, customers_report = (
            transform_customers(customers)
        )

        # Clean products
        products_clean, products_report = (
            transform_products(products)
        )

        # Clean orders
        orders_clean, orders_report = (
            transform_orders(orders)
        )

        # --------------------------------------------------
        # FOREIGN KEY INTEGRITY
        # --------------------------------------------------

        # Get valid customer IDs after transformation
        valid_customer_ids = set(
            customers_clean["customer_id"]
        )

        # Remove orders referencing customers
        # that no longer exist after transformation
        orders_clean = orders_clean[
            orders_clean["customer_id"].isin(
                valid_customer_ids
            )
        ].copy()

        # Get valid order IDs after transformation
        valid_order_ids = set(
            orders_clean["order_id"]
        )

        # Get valid product IDs after transformation
        valid_product_ids = set(
            products_clean["product_id"]
        )

        # Clean order items and keep only
        # valid foreign-key references
        order_items_clean, order_items_report = (
            transform_order_items(
                order_items,
                valid_order_ids=valid_order_ids,
                valid_product_ids=valid_product_ids,
            )
        )

        transformation_reports = [
            customers_report,
            products_report,
            orders_report,
            order_items_report,
        ]

        print(
            "Transformation completed."
        )

        print_transformation_summary(
            transformation_reports
        )

        logger.info(
            "Data transformation completed"
        )

        # --------------------------------------------------
        # 5. SAVE PROCESSED DATA
        # --------------------------------------------------

        print("\nSaving processed data...")

        logger.info(
            "Saving processed datasets"
        )

        customers_clean.to_csv(
            f"{PROCESSED_DATA_DIR}/customers_clean.csv",
            index=False,
        )

        products_clean.to_csv(
            f"{PROCESSED_DATA_DIR}/products_clean.csv",
            index=False,
        )

        orders_clean.to_csv(
            f"{PROCESSED_DATA_DIR}/orders_clean.csv",
            index=False,
        )

        order_items_clean.to_csv(
            f"{PROCESSED_DATA_DIR}/order_items_clean.csv",
            index=False,
        )

        print(
            "Processed data saved successfully."
        )

        logger.info(
            "Processed datasets saved successfully"
        )

        # --------------------------------------------------
        # 6. LOAD DATA INTO POSTGRESQL
        # --------------------------------------------------

        print(
            "\nLoading data into PostgreSQL..."
        )

        logger.info(
            "Starting PostgreSQL load"
        )

        if args.upsert:

            print(
                "Loading in UPSERT mode..."
            )

            logger.info(
                "Using upsert loading mode"
            )

            records_loaded = upsert_data()

            mode = "UPSERT"

        elif args.incremental:

            print(
                "Loading in INCREMENTAL mode..."
            )

            logger.info(
                "Using incremental loading mode"
            )

            records_loaded = (
                incremental_load_data()
            )

            mode = "INCREMENTAL"

        else:

            print(
                "Loading in FULL REFRESH mode..."
            )

            logger.info(
                "Using full refresh loading mode"
            )

            load_data()

            records_loaded = (
                len(customers_clean)
                + len(products_clean)
                + len(orders_clean)
                + len(order_items_clean)
            )

            mode = "FULL REFRESH"

        logger.info(
            "PostgreSQL load completed | "
            f"records_processed={records_loaded} | "
            f"mode={mode}"
        )

        # --------------------------------------------------
        # 7. RUN SQL ANALYTICS
        # --------------------------------------------------

        print("\nRunning SQL analytics...")

        logger.info(
            "Starting SQL analytics"
        )

        run_analytics()

        logger.info(
            "SQL analytics completed successfully"
        )

        # --------------------------------------------------
        # 8. COMPLETE PIPELINE RUN
        # --------------------------------------------------

        complete_pipeline_run(
            run_id,
            records_loaded
        )

        logger.info(
            f"Pipeline run completed successfully | "
            f"run_id={run_id} | "
            f"records_processed={records_loaded}"
        )

        # --------------------------------------------------
        # 9. FINAL OUTPUT
        # --------------------------------------------------

        print("\n")
        print("=" * 40)
        print("       PIPELINE COMPLETED")
        print("=" * 40)

        print(
            f"\nRun ID: {run_id}"
        )

        print(
            f"Records processed: {records_loaded}"
        )

        print(
            f"Mode: {mode}"
        )

        logger.info(
            "E-commerce ETL pipeline completed successfully"
        )

    except Exception:

        if run_id is not None:

            try:

                fail_pipeline_run(
                    run_id
                )

            except Exception:

                logger.exception(
                    "Failed to update pipeline run status"
                )

        logger.exception(
            "E-commerce ETL pipeline failed"
        )

        print("\n")
        print("=" * 40)
        print("         PIPELINE FAILED")
        print("=" * 40)

        raise


if __name__ == "__main__":

    args = parse_arguments()

    main(args)