import pandas as pd
import numpy as np
import time
import glob

class CreateTimeSeriesData:
    def __init__(self, target_cols: list) -> None:
        self.target_cols = target_cols
        self.dir_order_data = '../data/FEH_00100401_*.csv'
        self.dir_stock_data = '../data/TimeSeriesResult_*.csv'
        self.month_lists = list()
        self.months = list()
        self.base_df = pd.DataFrame()

    def load_data(self) -> pd.DataFrame:
        """対象データの読み込み"""        

        #機械受注長期時系列
        dir_order_data = glob.glob(self.dir_order_data)[0]
        order_data = pd.read_csv(dir_order_data, skiprows = 9, encoding='shift-jis') #2005年4月～2024年2月
        order_data = order_data.sort_values('時間軸(月次) コード')
        # numeric列は'xx,xxx'などのstr型格納されているのでfloat処理
        numeric_cols = order_data.columns[7:]
        # すべての列に対してカンマを取り除き、float型に変換
        for column in numeric_cols:
            order_data[column] = order_data[column].str.replace(',', '').astype(float)

        # 日経平均
        dir_stock_data = glob.glob(self.dir_stock_data)[0]
        stock_data = pd.read_csv(dir_stock_data)[63:-1] #2005年4月～2024年2月

        return order_data, stock_data
    
    def get_month_list(self, stock_data):
        """計算対象となるmonthのリストを取得"""
        
        self.month_lists = list(stock_data['時点'])
        self.months = self.month_lists[1:] # 階差を取得する関係で2005年5月以降の値を取得

    def rename_column(self, order_data: pd.DataFrame, stock_data: pd.DataFrame) -> pd.DataFrame:
        """加工対象のカラムを名前変更"""

        order_rename_dict = {
            '産業機械_産業用ロボット': 'Industrial_robots',
            '産業機械_風水力機械': 'Pneumatic_and_hydraulic_equipment',
            '産業機械_運搬機械': 'materialshandling_machinery',
            '産業機械_金属加工機械': 'Metal_working_machinery',
            '産業機械_冷凍機械': 'Refrigerating_machines',
            '産業機械_合成樹脂加工機械': 'Plastics_pocessing_machinery'
        }
        order_data = order_data.rename(columns=order_rename_dict)

        stock_data = stock_data.rename(columns={'日経平均株価【円】': 'stock'})

        return order_data, stock_data

    def logarithmic_diff_target(self, df: pd.DataFrame, tg_col: str) -> pd.DataFrame:
        """ターゲット指標に対しlog10で対数変換をした後に階差を取得"""
        
        df[tg_col] = np.log10(df[tg_col].astype(float)).diff()

        return df
    
    def logarithmic_target(self, df: pd.DataFrame, tg_col: str) -> pd.DataFrame:
        """ターゲット指標に対しlog10で対数変換のみ処理"""
        
        df[tg_col] = np.log10(df[tg_col].astype(float))

        return df

    def concat_dfs(self, order_data: pd.DataFrame, stock_data: pd.DataFrame) -> pd.DataFrame:
        """stock情報をLeft JOIN"""

        df = pd.merge(order_data, stock_data, left_on='時間軸(月次)', right_on='時点',how='left')

        return df

    def transposition_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """マート用にテーブルを転置"""

        # マート作成に用いるカラムのみ抽出
        use_cols = ['時間軸(月次)'] + self.target_cols
        df = df[use_cols]
        # 転置させてマートを作成
        df_t = df[use_cols].set_index('時間軸(月次)').rename_axis(None).T

        return df_t

    def create_base_df(self):
        """加工用のベースマートを作成"""
        order_data, stock_data = self.load_data()
        self.get_month_list(stock_data)
        order_data, stock_data = self.rename_column(order_data, stock_data)
        self.base_df = self.concat_dfs(order_data, stock_data)

    def create_original_df_pipeline(self) -> pd.DataFrame:
        """加工したデータフレーム（df_original）の取り出し"""   

        df = self.base_df.copy() # ベースマートを呼び出し
        for tg_col in self.target_cols:
            df = self.logarithmic_diff_target(df, tg_col)
        df = self.transposition_table(df)
        df = df[self.months]

        return df    
    
    def create_log_df_pipeline(self) -> pd.DataFrame:
        """加工したデータフレーム（df_log）の取り出し"""   

        df = self.base_df.copy() # ベースマートを呼び出し
        for tg_col in self.target_cols:
            df = self.logarithmic_target(df, tg_col)
        df = self.transposition_table(df)
        df = df[self.months]

        return df    