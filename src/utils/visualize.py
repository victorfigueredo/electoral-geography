from pathlib import Path
import os
import pandas as pd
import plotly.graph_objects as go


class Visualize:
    def __init__(
        self, data: pd.DataFrame, classified_candidates: pd.DataFrame, save_path=None
    ):
        self.data = data
        self.classified_candidates = classified_candidates
        if save_path is None:
            save_path = os.getcwd()
        self.save_path = Path(save_path) / "output"

    def create_file_path(self, candidate_name, uf, political_party, data_source):
        dir_path = self.save_path / data_source / "electoral_geography"
        dir_path.mkdir(parents=True, exist_ok=True)

        # Clean candidate name, uf and party for usage in file name
        clean_candidate_name = candidate_name.replace(
            " ", "_"
        )  # Replace space with underscore
        clean_candidate_name = "".join(
            e for e in clean_candidate_name if e.isalnum() or e == "_"
        )  # Remove non-alphanumeric characters, excluding underscore
        clean_uf = "".join(e for e in uf if e.isalnum())
        clean_party = "".join(e for e in political_party if e.isalnum())

        # Create file name
        file_name = f"{clean_candidate_name}_{clean_party}_{clean_uf}_treemap.png"

        return dir_path / file_name

    def plot_elected_official_treemap(
        self, nm_urna_candidato: str, data_source: str = "tse"
    ) -> None:
        if data_source == "tse":
            valid_votes_col = "qt_votos_nom_validos"
            official_data = self.data[
                (self.data["ds_sit_totalizacao"] == "Eleito")
                & (self.data["nm_urna_candidato"] == nm_urna_candidato)
            ].copy()
        elif data_source == "twitter":
            valid_votes_col = "qt_city_mentions"
            official_data = self.data[
                (self.data["nm_urna_candidato"] == nm_urna_candidato)
            ].copy()
        else:
            raise ValueError(
                f"Invalid data_source '{data_source}'. Valid options are 'tse' and 'twitter'."
            )

        if official_data[valid_votes_col].sum() == 0:
            print(f"No data available for candidate {nm_urna_candidato}.")
            return

        candidate_quadrant = self.classified_candidates.loc[
            self.classified_candidates["nm_urna_candidato"] == nm_urna_candidato,
            "voting_type",
        ].iloc[0]

        official_data.loc[:, "voting_type"] = candidate_quadrant

        fig = go.Figure(
            go.Treemap(
                labels=official_data["nm_municipio"],
                text=official_data["dominance_index"],
                parents=official_data["sg_ue"],
                values=official_data[valid_votes_col],
                marker=dict(
                    colors=official_data["dominance_index"],
                    colorscale="Reds",
                ),
                textinfo="label+value",
                hovertemplate=f"<b>%{{label}}</b><br>{valid_votes_col}: %{{value}}<br>dominance_index: %{{text:.2f}}<extra></extra>",
            )
        )

        # Get party and uf from the first non-null entry
        sg_partido = official_data["sg_partido"].dropna().values[0]
        sg_ue = official_data["sg_ue"].dropna().values[0]

        fig.update_layout(
            title=f"{nm_urna_candidato} ({sg_partido}/{sg_ue}), classificação {candidate_quadrant}, {data_source}",
            margin=dict(t=30, l=0, r=0, b=0),
            width=1000,
            height=600,
        )

        # Create the file path
        file_path = self.create_file_path(
            nm_urna_candidato, sg_ue, sg_partido, data_source
        )

        fig.write_image(str(file_path), scale=2)
        print(f"Treemap saved as: {file_path}")

    def generate_visualizations(self, data_source: str = "tse") -> None:
        assert data_source in [
            "tse",
            "twitter",
        ], "Invalid data_source, should be 'tse' or 'twitter'."

        candidates = self.classified_candidates["nm_urna_candidato"].unique()

        for candidate in candidates:
            self.plot_elected_official_treemap(candidate, data_source)
