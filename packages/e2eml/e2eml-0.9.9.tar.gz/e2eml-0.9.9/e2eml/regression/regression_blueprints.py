from e2eml.regression.regression_models import RegressionModels
from e2eml.full_processing.cpu_processing_nlp import NlpPreprocessing
import logging


class RegressionBluePrint(RegressionModels, NlpPreprocessing):
    """
    Runs a blue print from preprocessing to model training. Can be used as a pipeline to predict on new data,
    if the predict_mode attribute is True.
    This class stores all regression blueprints.
    :param preprocessing_type: Select the type of preprocessing pipeline. "Minimum" executes the least possible steps,
    "full" the whole standard preprocessing and "nlp" adds functionality especially for NLP tasks.
    :param df: Accepts a dataframe to make predictions on new data.

    This class also stores all model training and prediction methods for regression tasks (inherited).
    This class also stores all pipeline relevant information (inherited from cpu preprocessing).
    The attribute "df_dict" always holds train and test as well as to predict data. The attribute
    "preprocess_decisions" stores encoders and other information generated during the
    model training. The attributes "predicted_classes" and "predicted_probs" store dictionaries (model names are dictionary keys)
    with predicted classes and probabilities (classification tasks) while "predicted_values" stores regression based
    predictions. The attribute "evaluation_scores" keeps track of model evaluation metrics (in dictionary format).
    :param datasource: Expects a Pandas dataframe (containing the target feature as a column)
    :param target_variable: Name of the target feature's column within the datasource dataframe.
    :param date_columns: Date columns can be passed as lists additionally for respective preprocessing. If not provided
    e2eml will try to detect datetime columns automatically. Date format is expected as YYYY-MM-DD anyway.
    :param categorical_columns: Categorical columns can be passed as lists additionally for respective preprocessing.
    If not provided e2eml will try to detect categorical columns automatically.
    :param nlp_columns: NLP columns can be passed specifically. This only makes sense, if the chosen blueprint runs under 'nlp' processing.
    If NLP columns are not declared, categorical columns will be interpreted as such.
    :param unique_identifier: A unique identifier (i.e. an ID column) can be passed as well to preserve this information
     for later processing.
    :param ml_task: Can be 'binary', 'multiclass' or 'regression'. On default will be determined automatically.
    :param preferred_training_mode: Must be 'cpu', if e2eml has been installed into an environment without LGBM and Xgboost on GPU.
    Can be set to 'gpu', if LGBM and Xgboost have been installed with GPU support. The default 'auto' will detect GPU support
    and optimize accordingly. (Default: 'auto')
    :param tune_mode: 'Accurate' will lead use K-fold cross validation per hyperparameter set durig optimization. 'Simple'
    will make use of use 1-fold validation only, which leads to much faster training times.
    :param logging_file_path: Preferred location to save the log file. Will otherwise stored in the current folder.
    :param low_memory_mode: Adds a preprocessing feature to reduce dataframe memory footprint. Will lead to a loss in
    model performance. Will be extended by further memory savings features in future releases.
    However we highly recommend GPU usage to heavily decrease model training times.
    :return: Updates class attributes by its predictions.
    """
    def full_regression_preprocessing(self, df=None, preprocessing_type='full'):
        """
        Runs a preprocessing blueprint only. This is useful for building custom pipelines.
        :param df: Accepts a dataframe to run ml preprocessing on it.
        :param preprocessing_type: Select the type of preprocessing pipeline. "Minimum" executes the least possible steps,
        "full" the whole standard preprocessing and "nlp" adds functionality especially for NLP tasks.
        :return: Updates class attributes.
        """
        logging.info('Start blueprint.')
        try:
            if df.empty:
                skip_train = False
            else:
                self.dataframe = df
                skip_train = True
        except AttributeError:
            skip_train = False
        self.train_test_split(how=self.train_split_type)
        self.datetime_converter(datetime_handling='all')
        if preprocessing_type == 'nlp':
            self.pos_tagging_pca()
        self.rare_feature_processor(threshold=0.03, mask_as='miscellaneous')
        self.cardinality_remover(threshold=100)
        self.onehot_pca()
        self.category_encoding(algorithm='target')
        self.delete_high_null_cols(threshold=0.5)
        self.fill_nulls(how='static')
        self.data_binning(nb_bins=10)
        #self.skewness_removal()
        self.outlier_care(method='isolation', how='append')
        self.remove_collinearity(threshold=0.8)
        self.clustering_as_a_feature(algorithm='dbscan', eps=0.3, n_jobs=-1, min_samples=10)
        for nb_cluster in range(2, 10):
            self.clustering_as_a_feature(algorithm='kmeans', nb_clusters=nb_cluster)
        if self.low_memory_mode:
            self.reduce_memory_footprint()
        self.automated_feature_selection(metric='logloss')
        self.sort_columns_alphabetically()

    def train_pred_selected_model(self, algorithm=None, skip_train=False):
        logging.info(f'Start ML training {algorithm}')
        if algorithm == 'xgboost':
            # train Xgboost
            if skip_train:
                pass
            else:
                self.xg_boost_train(autotune=True, tune_mode=self.tune_mode)
            self.xgboost_predict(feat_importance=False)
            self.regression_eval(algorithm=algorithm)
        elif algorithm == 'ngboost':
            # train Ngboost
            if skip_train:
                pass
            else:
                self.ngboost_train(tune_mode=self.tune_mode)
            self.ngboost_predict(feat_importance=True, importance_alg='permutation')
            self.regression_eval(algorithm=algorithm)
        elif algorithm == 'lgbm':
            # train LGBM
            if skip_train:
                pass
            else:
                try:
                    self.lgbm_train(tune_mode=self.tune_mode)
                except Exception:
                    self.lgbm_train(tune_mode=self.tune_mode)
            self.lgbm_predict(feat_importance=False)
            self.regression_eval(algorithm=algorithm)
        elif algorithm == 'sklearn_ensemble':
            # train sklearn ensemble
            if skip_train:
                pass
            else:
                self.sklearn_ensemble_train()
            self.sklearn_ensemble_predict(feat_importance=True, importance_alg='permutation')
            algorithm = 'sklearn_ensemble'
            self.regression_eval(algorithm=algorithm)

    def ml_bp10_train_test_regression_full_processing_linear_reg(self, df=None, preprocessing_type='full'):
        """
        Runs a blue print from preprocessing to model training. Can be used as a pipeline to predict on new data,
        if the predict_mode attribute is True.
        :param df: Accepts a dataframe to make predictions on new data.
        :param preprocessing_type: Select the type of preprocessing pipeline. "Minimum" executes the least possible steps,
        "full" the whole standard preprocessing and "nlp" adds functionality especially for NLP tasks.
        :return: Updates class attributes by its predictions.
        """
        logging.info('Start blueprint.')
        try:
            if df.empty:
                skip_train = False
            else:
                self.dataframe = df
                skip_train = True
        except AttributeError:
            skip_train = False
        self.train_test_split(how=self.train_split_type)
        self.datetime_converter(datetime_handling='all')
        if preprocessing_type == 'nlp':
            self.pos_tagging_pca()
        self.rare_feature_processor(threshold=0.03, mask_as='miscellaneous')
        self.cardinality_remover(threshold=100)
        self.onehot_pca()
        self.category_encoding(algorithm='target')
        self.delete_high_null_cols(threshold=0.5)
        self.fill_nulls(how='static')
        self.data_binning(nb_bins=10)
        self.skewness_removal()
        self.outlier_care(method='isolation', how='append')
        self.remove_collinearity(threshold=0.8)
        self.clustering_as_a_feature(algorithm='dbscan', eps=0.3, n_jobs=-1, min_samples=10)
        for nb_cluster in range(2, 10):
            self.clustering_as_a_feature(algorithm='kmeans', nb_clusters=nb_cluster)
        if self.low_memory_mode:
            self.reduce_memory_footprint()
        self.automated_feature_selection(metric='mae')
        self.sort_columns_alphabetically()
        if skip_train:
            pass
        else:
            self.linear_regression_train()
        self.data_scaling()
        algorithm = 'linear_regression'
        self.linear_regression_predict(feat_importance=True, importance_alg='permutation')
        self.regression_eval(algorithm=algorithm)
        self.prediction_mode = True
        logging.info('Finished blueprint.')

    def ml_bp11_regression_full_processing_xgboost(self, df=None, preprocessing_type='full'):
        """
        Runs a blue print from preprocessing to model training. Can be used as a pipeline to predict on new data,
        if the predict_mode attribute is True.
        :param df: Accepts a dataframe to make predictions on new data.
        :param preprocessing_type: Select the type of preprocessing pipeline. "Minimum" executes the least possible steps,
        "full" the whole standard preprocessing and "nlp" adds functionality especially for NLP tasks.
        :return: Updates class attributes by its predictions.
        """
        logging.info('Start blueprint.')
        try:
            if df.empty:
                skip_train = False
            else:
                self.dataframe = df
                skip_train = True
        except AttributeError:
            skip_train = False
        self.train_test_split(how=self.train_split_type)
        self.datetime_converter(datetime_handling='all')
        if preprocessing_type == 'nlp':
            self.pos_tagging_pca()
        self.rare_feature_processor(threshold=0.03, mask_as='miscellaneous')
        self.cardinality_remover(threshold=100)
        self.onehot_pca()
        self.category_encoding(algorithm='target')
        self.delete_high_null_cols(threshold=0.5)
        self.fill_nulls(how='static')
        self.data_binning(nb_bins=10)
        #self.skewness_removal()
        self.outlier_care(method='isolation', how='append')
        self.remove_collinearity(threshold=0.8)
        self.clustering_as_a_feature(algorithm='dbscan', eps=0.3, n_jobs=-1, min_samples=10)
        for nb_cluster in range(2, 10):
            self.clustering_as_a_feature(algorithm='kmeans', nb_clusters=nb_cluster)
        if self.low_memory_mode:
            self.reduce_memory_footprint()
        self.automated_feature_selection(metric='mae')
        self.sort_columns_alphabetically()
        if skip_train:
            pass
        else:
            self.xg_boost_train(autotune=True)
        self.xgboost_predict(feat_importance=True)
        self.regression_eval('xgboost')
        self.prediction_mode = True
        logging.info('Finished blueprint.')

    def ml_bp12_regressions_full_processing_lgbm(self, df=None, preprocessing_type='nlp'):
        """
        Runs a blue print from preprocessing to model training. Can be used as a pipeline to predict on new data,
        if the predict_mode attribute is True.
        :param df: Accepts a dataframe to make predictions on new data.
        :param preprocessing_type: Select the type of preprocessing pipeline. "Minimum" executes the least possible steps,
        "full" the whole standard preprocessing and "nlp" adds functionality especially for NLP tasks.
        :return: Updates class attributes by its predictions.
        """
        logging.info('Start blueprint.')
        try:
            if df.empty:
                skip_train = False
            else:
                self.dataframe = df
                skip_train = True
        except AttributeError:
            skip_train = False
        self.train_test_split(how=self.train_split_type)
        self.datetime_converter(datetime_handling='all')
        if preprocessing_type == 'nlp':
            self.pos_tagging_pca()
        self.rare_feature_processor(threshold=0.03, mask_as='miscellaneous')
        self.cardinality_remover(threshold=100)
        self.onehot_pca()
        self.category_encoding(algorithm='target')
        self.delete_high_null_cols(threshold=0.5)
        self.fill_nulls(how='static')
        self.data_binning(nb_bins=10)
        #self.skewness_removal()
        self.outlier_care(method='isolation', how='append')
        self.remove_collinearity(threshold=0.8)
        self.clustering_as_a_feature(algorithm='dbscan', eps=0.3, n_jobs=-1, min_samples=10)
        for nb_cluster in range(2, 10):
            self.clustering_as_a_feature(algorithm='kmeans', nb_clusters=nb_cluster)
        if self.low_memory_mode:
            self.reduce_memory_footprint()
        self.automated_feature_selection(metric='mae')
        self.sort_columns_alphabetically()
        if skip_train:
            pass
        else:
            self.lgbm_train(tune_mode=self.tune_mode)
        self.lgbm_predict(feat_importance=True)
        self.regression_eval('lgbm')
        self.prediction_mode = True
        logging.info('Finished blueprint.')

    def ml_bp13_regression_full_processing_sklearn_stacking_ensemble(self, df=None, preprocessing_type='full'):
        """
        Runs a blue print from preprocessing to model training. Can be used as a pipeline to predict on new data,
        if the predict_mode attribute is True.
        :param df: Accepts a dataframe to make predictions on new data.
        :param preprocessing_type: Select the type of preprocessing pipeline. "Minimum" executes the least possible steps,
        "full" the whole standard preprocessing and "nlp" adds functionality especially for NLP tasks.
        :return: Updates class attributes by its predictions.
        """
        logging.info('Start blueprint.')
        try:
            if df.empty:
                skip_train = False
            else:
                self.dataframe = df
                skip_train = True
        except AttributeError:
            skip_train = False
        self.train_test_split(how=self.train_split_type)
        self.datetime_converter(datetime_handling='all')
        if preprocessing_type == 'nlp':
            self.pos_tagging_pca()
        self.rare_feature_processor(threshold=0.03, mask_as='miscellaneous')
        self.cardinality_remover(threshold=100)
        self.onehot_pca()
        self.category_encoding(algorithm='target')
        self.delete_high_null_cols(threshold=0.5)
        self.fill_nulls(how='static')
        self.data_binning(nb_bins=10)
        #self.skewness_removal()
        self.outlier_care(method='isolation', how='append')
        self.remove_collinearity(threshold=0.8)
        self.clustering_as_a_feature(algorithm='dbscan', eps=0.3, n_jobs=-1, min_samples=10)
        for nb_cluster in range(2, 10):
            self.clustering_as_a_feature(algorithm='kmeans', nb_clusters=nb_cluster)
        if self.low_memory_mode:
            self.reduce_memory_footprint()
        self.automated_feature_selection(metric='mae')
        self.sort_columns_alphabetically()
        self.data_scaling()
        if skip_train:
            pass
        else:
            self.sklearn_ensemble_train()
        self.sklearn_ensemble_predict(feat_importance=True, importance_alg='permutation')
        algorithm = 'sklearn_ensemble'
        self.regression_eval('sklearn_ensemble')
        self.prediction_mode = True
        logging.info('Finished blueprint.')

    def ml_bp14_regressions_full_processing_ngboost(self, df=None, preprocessing_type='full'):
        """
        Runs a blue print from preprocessing to model training. Can be used as a pipeline to predict on new data,
        if the predict_mode attribute is True.
        :param df: Accepts a dataframe to make predictions on new data.
        :param preprocessing_type: Select the type of preprocessing pipeline. "Minimum" executes the least possible steps,
        "full" the whole standard preprocessing and "nlp" adds functionality especially for NLP tasks.
        :return: Updates class attributes by its predictions.
        """
        logging.info('Start blueprint.')
        try:
            if df.empty:
                skip_train = False
            else:
                self.dataframe = df
                skip_train = True
        except AttributeError:
            skip_train = False
        self.train_test_split()
        self.datetime_converter(datetime_handling='all')
        if preprocessing_type == 'nlp':
            self.pos_tagging_pca()
        self.rare_feature_processor(threshold=0.03, mask_as='miscellaneous')
        self.cardinality_remover(threshold=100)
        self.onehot_pca()
        self.category_encoding(algorithm='target')
        self.delete_high_null_cols(threshold=0.5)
        self.fill_nulls(how='static')
        self.data_binning(nb_bins=10)
        #self.skewness_removal()
        self.outlier_care(method='isolation', how='append')
        self.remove_collinearity(threshold=0.8)
        self.clustering_as_a_feature(algorithm='dbscan', eps=0.3, n_jobs=-1, min_samples=10)
        for nb_cluster in range(2, 10):
            self.clustering_as_a_feature(algorithm='kmeans', nb_clusters=nb_cluster)
        if self.low_memory_mode:
            self.reduce_memory_footprint()
        self.automated_feature_selection(metric='mae')
        self.sort_columns_alphabetically()
        if skip_train:
            pass
        else:
            self.ngboost_train(tune_mode=self.tune_mode)
        self.ngboost_predict(feat_importance=False, importance_alg='permutation')
        self.regression_eval('ngboost')
        self.prediction_mode = True
        logging.info('Finished blueprint.')

    def ml_special_regression_full_processing_boosting_blender(self, df=None, preprocessing_type='full'):
        """
        Runs a blue print from preprocessing to model training. Can be used as a pipeline to predict on new data,
        if the predict_mode attribute is True.
        :param df: Accepts a dataframe to make predictions on new data.
        :param preprocessing_type: Select the type of preprocessing pipeline. "Minimum" executes the least possible steps,
        "full" the whole standard preprocessing and "nlp" adds functionality especially for NLP tasks.
        :return: Updates class attributes by its predictions.
        """
        logging.info('Start blueprint.')
        try:
            if df.empty:
                skip_train = False
            else:
                self.dataframe = df
                skip_train = True
        except AttributeError:
            skip_train = False
        self.train_test_split(how=self.train_split_type)
        self.datetime_converter(datetime_handling='all')
        if preprocessing_type == 'nlp':
            self.pos_tagging_pca()
        self.rare_feature_processor(threshold=0.03, mask_as='miscellaneous')
        self.cardinality_remover(threshold=100)
        self.onehot_pca()
        self.category_encoding(algorithm='target')
        self.delete_high_null_cols(threshold=0.5)
        self.fill_nulls(how='static')
        self.data_binning(nb_bins=10)
        #self.skewness_removal()
        self.outlier_care(method='isolation', how='append')
        self.remove_collinearity(threshold=0.8)
        self.clustering_as_a_feature(algorithm='dbscan', eps=0.3, n_jobs=-1, min_samples=10)
        for nb_cluster in range(2, 10):
            self.clustering_as_a_feature(algorithm='kmeans', nb_clusters=nb_cluster)
        if self.low_memory_mode:
            self.reduce_memory_footprint()
        self.automated_feature_selection(metric='logloss')
        self.sort_columns_alphabetically()
        if skip_train:
            pass
        else:
            self.ngboost_train(tune_mode=self.tune_mode)
            self.lgbm_train(tune_mode=self.tune_mode)
            self.xg_boost_train(autotune=True, tune_mode=self.tune_mode)
        self.ngboost_predict(feat_importance=True, importance_alg='SHAP')
        self.lgbm_predict(feat_importance=True)
        self.xgboost_predict(feat_importance=True)
        if self.prediction_mode:
            self.dataframe["lgbm_preds"] = self.predicted_values[f"lgbm"]
            self.dataframe["ngboost_preds"] = self.predicted_values[f"ngboost"]
            self.dataframe["xgboost_preds"] = self.predicted_values[f"xgboost"]
            self.dataframe["blended_preds"] = (self.dataframe["lgbm_preds"] + self.dataframe["ngboost_preds"] + self.dataframe["xgboost_preds"])/3
            self.predicted_values[f"blended_preds"] = self.dataframe["blended_preds"]
        else:
            X_train, X_test, Y_train, Y_test = self.unpack_test_train_dict()
            X_test["lgbm_preds"] = self.predicted_values[f"lgbm"]
            X_test["ngboost_preds"] = self.predicted_values[f"ngboost"]
            X_test["xgboost_preds"] = self.predicted_values[f"xgboost"]
            X_test["blended_preds"] = (X_test["lgbm_preds"] + X_test["ngboost_preds"] + X_test["xgboost_preds"])/3
            self.predicted_values[f"blended_preds"] = X_test["blended_preds"]
        self.classification_eval('blended_preds')
        self.prediction_mode = True
        logging.info('Finished blueprint.')

    def ml_special_regression_auto_model_exploration(self, df=None, preprocessing_type='full'):
        """
        Runs a blue print from preprocessing to model training. Can be used as a pipeline to predict on new data,
        if the predict_mode attribute is True.
        :param df: Accepts a dataframe to make predictions on new data.
        :param preprocessing_type: Select the type of preprocessing pipeline. "Minimum" executes the least possible steps,
        "full" the whole standard preprocessing and "nlp" adds functionality especially for NLP tasks.
        :return: Updates class attributes by its predictions.
        """
        logging.info('Start blueprint.')
        try:
            if df.empty:
                skip_train = False
            else:
                self.dataframe = df
                skip_train = True
        except AttributeError:
            skip_train = False
        self.train_test_split(how=self.train_split_type)
        self.datetime_converter(datetime_handling='all')
        if preprocessing_type == 'nlp':
            self.pos_tagging_pca()
        self.rare_feature_processor(threshold=0.03, mask_as='miscellaneous')
        self.cardinality_remover(threshold=100)
        self.onehot_pca()
        self.category_encoding(algorithm='target')
        self.delete_high_null_cols(threshold=0.5)
        self.fill_nulls(inplace=False, how='static')
        self.data_binning(nb_bins=10)
        #self.skewness_removal()
        self.outlier_care(method='isolation', how='append')
        self.remove_collinearity(threshold=0.8)
        self.clustering_as_a_feature(algorithm='dbscan', eps=0.3, n_jobs=-1, min_samples=10)
        for nb_cluster in range(2, 10):
            self.clustering_as_a_feature(algorithm='kmeans', nb_clusters=nb_cluster)
        if self.low_memory_mode:
            self.reduce_memory_footprint()
        self.automated_feature_selection(metric='logloss')
        self.sort_columns_alphabetically()
        if not self.prediction_mode:
            self.train_pred_selected_model(algorithm='lgbm')
            self.train_pred_selected_model(algorithm='xgboost')
            self.train_pred_selected_model(algorithm='ngboost')
            self.train_pred_selected_model(algorithm='sklearn_ensemble')

            # select best model
            max_matthews = 0
            self.best_model = 'xgboost'
            for k, v in self.evaluation_scores.items():
                if max_matthews < (v['matthews']):
                    max_matthews = (v['matthews'])
                    self.best_model = k
            self.train_pred_selected_model(algorithm=self.best_model)
            self.prediction_mode = True
        else:
            self.train_pred_selected_model(algorithm=self.best_model, skip_train=skip_train)
        logging.info('Finished blueprint.')