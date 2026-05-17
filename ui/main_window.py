# Nama  : Dodi Wijaya
# NIM   : F1D02310047
# Kelas : Pemrograman Visual D

import pandas as pd

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton,
    QComboBox, QTableWidget,
    QTableWidgetItem, QFileDialog,
    QMessageBox, QHeaderView,
    QFrame, QGraphicsDropShadowEffect,
    QTabWidget
)

from PySide6.QtCore import Qt

from ui.chart_widget import ChartWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "📊 Dashboard Visualisasi Data"
        )

        self.resize(1500, 900)

        self.setMinimumSize(1250, 750)

        self.load_data()

        self.setup_ui()

        self.filtered_df = self.df.copy()

        self.load_table()

        self.update_dashboard()

        self.load_charts()

    def load_data(self):

        try:

            self.df = pd.read_csv(
                "data/supermarket_sales.csv"
            )

            self.df.rename(
                columns={
                    "Customer type": "Customer Type",
                    "Product line": "Product Line",
                    "Unit price": "Unit Price",
                    "Tax 5%": "Tax 5%",
                    "gross margin percentage": "Gross Margin Percentage",
                    "gross income": "Gross Income",
                    "cogs": "COGS",
                    "Rating": "Customer Rating"
                },
                inplace=True
            )

            if (
                "Total" in self.df.columns
                and "Sales" not in self.df.columns
            ):

                self.df.rename(
                    columns={"Total": "Sales"},
                    inplace=True
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Gagal memuat dataset!\n{e}"
            )

            self.df = pd.DataFrame()

    def add_shadow(self, widget):

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(25)

        shadow.setXOffset(0)

        shadow.setYOffset(4)

        shadow.setColor(Qt.black)

        widget.setGraphicsEffect(shadow)

    def setup_ui(self):

        container = QWidget()

        self.setCentralWidget(container)

        main_layout = QVBoxLayout(container)

        main_layout.setContentsMargins(
            20, 20, 20, 20
        )

        main_layout.setSpacing(16)

        title = QLabel(
            "📊 Supermarket Sales Dashboard"
        )

        title.setObjectName("main_title")

        main_layout.addWidget(title)

        card_layout = QHBoxLayout()

        card_layout.setSpacing(18)

        self.sales_card = QLabel()

        self.transaction_card = QLabel()

        self.rating_card = QLabel()

        for card in [
            self.sales_card,
            self.transaction_card,
            self.rating_card
        ]:

            card.setObjectName(
                "dashboard_card"
            )

            card.setAlignment(
                Qt.AlignCenter
            )

            self.add_shadow(card)

            card_layout.addWidget(card)

        main_layout.addLayout(card_layout)

        filter_layout = QHBoxLayout()

        filter_layout.setSpacing(12)

        self.city_filter = QComboBox()

        self.customer_filter = QComboBox()

        self.gender_filter = QComboBox()

        self.payment_filter = QComboBox()

        self.city_filter.addItems(
            ["All City"] +
            sorted(
                self.df["City"].unique()
            )
        )

        self.customer_filter.addItems(
            ["All Customer"] +
            sorted(
                self.df[
                    "Customer Type"
                ].unique()
            )
        )

        self.gender_filter.addItems(
            ["All Gender"] +
            sorted(
                self.df["Gender"].unique()
            )
        )

        self.payment_filter.addItems(
            ["All Payment"] +
            sorted(
                self.df["Payment"].unique()
            )
        )

        filter_layout.addWidget(
            QLabel("🏙 City")
        )

        filter_layout.addWidget(
            self.city_filter
        )

        filter_layout.addWidget(
            QLabel("👥 Customer")
        )

        filter_layout.addWidget(
            self.customer_filter
        )

        filter_layout.addWidget(
            QLabel("🚻 Gender")
        )

        filter_layout.addWidget(
            self.gender_filter
        )

        filter_layout.addWidget(
            QLabel("💳 Payment")
        )

        filter_layout.addWidget(
            self.payment_filter
        )

        filter_layout.addStretch()

        self.refresh_btn = QPushButton(
            "🔄 Refresh Dashboard"
        )

        self.refresh_btn.setObjectName(
            "btn_refresh"
        )

        self.refresh_btn.clicked.connect(
            self.apply_filter
        )

        self.export_btn = QPushButton(
            "💾 Export PNG"
        )

        self.export_btn.setObjectName(
            "btn_export"
        )

        self.export_btn.clicked.connect(
            self.export_chart
        )

        filter_layout.addWidget(
            self.refresh_btn
        )

        filter_layout.addWidget(
            self.export_btn
        )

        main_layout.addLayout(
            filter_layout
        )

        self.filter_info = QLabel(
            "Menampilkan semua data"
        )

        self.filter_info.setObjectName(
            "filter_info"
        )

        main_layout.addWidget(
            self.filter_info
        )

        self.tabs = QTabWidget()

        self.chart_tab = QWidget()

        self.table_tab = QWidget()

        self.tabs.addTab(
            self.chart_tab,
            "📈 Visualization"
        )

        self.tabs.addTab(
            self.table_tab,
            "📋 Data Table"
        )

        self.setup_chart_tab()

        self.setup_table_tab()

        main_layout.addWidget(self.tabs)

        main_layout.setStretch(4, 1)

    def setup_chart_tab(self):

        layout = QHBoxLayout(self.chart_tab)

        layout.setSpacing(18)

        chart_frame1 = QFrame()

        chart_frame2 = QFrame()

        chart_frame1.setObjectName(
            "chart_frame"
        )

        chart_frame2.setObjectName(
            "chart_frame"
        )

        self.add_shadow(chart_frame1)

        self.add_shadow(chart_frame2)

        chart1_layout = QVBoxLayout(
            chart_frame1
        )

        chart2_layout = QVBoxLayout(
            chart_frame2
        )

        self.bar_chart = ChartWidget()

        self.pie_chart = ChartWidget()

        chart1_layout.addWidget(
            self.bar_chart
        )

        chart2_layout.addWidget(
            self.pie_chart
        )

        layout.addWidget(
            chart_frame1,
            stretch=6
        )

        layout.addWidget(
            chart_frame2,
            stretch=4
        )

    def setup_table_tab(self):

        layout = QVBoxLayout(self.table_tab)

        self.table = QTableWidget()

        self.table.setColumnCount(
            len(self.df.columns)
        )

        self.table.setHorizontalHeaderLabels(
            self.df.columns
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Interactive
        )

        self.table.horizontalHeader().setStretchLastSection(
            True
        )

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.setShowGrid(False)

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setStyleSheet("""
            QTableCornerButton::section {
                background: #111827;
                border: none;
            }
        """)

        layout.addWidget(self.table)

    def apply_filter(self):

        df = self.df.copy()

        city = self.city_filter.currentText()

        customer = (
            self.customer_filter.currentText()
        )

        gender = (
            self.gender_filter.currentText()
        )

        payment = (
            self.payment_filter.currentText()
        )

        if city != "All City":

            df = df[df["City"] == city]

        if customer != "All Customer":

            df = df[
                df["Customer Type"] == customer
            ]

        if gender != "All Gender":

            df = df[
                df["Gender"] == gender
            ]

        if payment != "All Payment":

            df = df[
                df["Payment"] == payment
            ]

        self.filtered_df = df

        self.load_table()

        self.update_dashboard()

        self.load_charts()

        filter_text = (
            f"City: {city} | "
            f"Customer: {customer} | "
            f"Gender: {gender} | "
            f"Payment: {payment}"
        )

        self.filter_info.setText(filter_text)

    def load_table(self):

        self.table.setRowCount(0)

        for row, data in enumerate(
            self.filtered_df.values
        ):

            self.table.insertRow(row)

            for col, value in enumerate(data):

                item = QTableWidgetItem(
                    str(value)
                )

                item.setTextAlignment(
                    Qt.AlignCenter
                )

                self.table.setItem(
                    row,
                    col,
                    item
                )

    def update_dashboard(self):

        total_sales = (
            self.filtered_df["Sales"].sum()
        )

        total_transaction = (
            len(self.filtered_df)
        )

        avg_rating = (
            self.filtered_df["Customer Rating"].mean()
        )

        self.sales_card.setText(
            f"💰 Total Sales\n${total_sales:,.2f}"
        )

        self.transaction_card.setText(
            f"🛒 Transactions\n{total_transaction}"
        )

        self.rating_card.setText(
            f"⭐ Avg Rating\n{avg_rating:.2f}"
        )

    def load_charts(self):

        self.bar_chart.clear_chart()

        product_sales = (
            self.filtered_df.groupby(
                "Product Line"
            )["Sales"]
            .sum()
            .sort_values()
        )

        self.bar_chart.axes.bar(
            product_sales.index,
            product_sales.values,
            color="#7C3AED"
        )

        self.bar_chart.axes.set_title(
            "Sales by Product Line",
            color="#111827",
            fontweight="bold"
        )

        self.bar_chart.axes.tick_params(
            axis="x",
            rotation=15,
            colors="#334155",
            labelsize=9
        )

        self.bar_chart.axes.spines[
            'top'
        ].set_visible(False)

        self.bar_chart.axes.spines[
            'right'
        ].set_visible(False)

        self.bar_chart.draw_chart()

        self.pie_chart.clear_chart()

        payment_data = (
            self.filtered_df["Payment"]
            .value_counts()
        )

        self.pie_chart.axes.pie(
            payment_data.values,
            labels=payment_data.index,
            autopct="%1.1f%%",
            colors=[
                "#7C3AED",
                "#06B6D4",
                "#F59E0B"
            ]
        )

        self.pie_chart.axes.set_title(
            "Payment Distribution",
            color="#111827",
            fontweight="bold"
        )

        self.pie_chart.draw_chart()

    def export_chart(self):

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Chart",
            "dashboard_chart.png",
            "PNG Files (*.png)"
        )

        if path:

            from matplotlib.figure import Figure

            from matplotlib.backends.backend_agg import (
                FigureCanvasAgg
            )

            figure = Figure(
                figsize=(14, 6)
            )

            canvas = FigureCanvasAgg(figure)

            ax1 = figure.add_subplot(121)

            ax2 = figure.add_subplot(122)

            product_sales = (
                self.filtered_df.groupby(
                    "Product Line"
                )["Sales"]
                .sum()
                .sort_values()
            )

            ax1.bar(
                product_sales.index,
                product_sales.values,
                color="#7C3AED"
            )

            ax1.set_title(
                "Sales by Product Line",
                fontweight="bold",
                color="#111827"
            )

            ax1.tick_params(
                axis="x",
                rotation=15,
                labelsize=9
            )

            ax1.spines['top'].set_visible(False)

            ax1.spines['right'].set_visible(False)

            payment_data = (
                self.filtered_df["Payment"]
                .value_counts()
            )

            ax2.pie(
                payment_data.values,
                labels=payment_data.index,
                autopct="%1.1f%%",
                colors=[
                    "#7C3AED",
                    "#06B6D4",
                    "#F59E0B"
                ]
            )

            ax2.set_title(
                "Payment Distribution",
                fontweight="bold",
                color="#111827"
            )

            figure.tight_layout()

            figure.savefig(
                path,
                dpi=150,
                facecolor="white"
            )

            QMessageBox.information(
                self,
                "Success",
                "Semua chart berhasil disimpan!"
            )