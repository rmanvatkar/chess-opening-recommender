import pandas as pd

class OpeningDataLoader:
    def __init__(self, original_csv: str, processed_csv: str):
        self.original_csv = original_csv
        self.processed_csv = processed_csv

    def load_and_process(self):
        df = pd.read_csv(
            self.original_csv,
            encoding="utf-8",
            on_bad_lines="skip",
        ).fillna("")
        required_columns = (
            "name",
            "eco",
            "moves",
            "style_tags",
            "difficulty",
            "plays_as",
            "key_ideas",
            "description",
        )

        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(sorted(missing_columns))}")

        df["combined_info"] = df.apply(
            lambda row: "\n".join(
                f"{column.replace('_', ' ').title()}: {row[column]}"
                for column in required_columns
                if row[column]
            ),
            axis=1,
        )

        df[["combined_info"]].to_csv(
            self.processed_csv,
            index=False,
            encoding="utf-8",
        )

        return self.processed_csv
