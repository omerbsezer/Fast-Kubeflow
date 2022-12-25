import kfp
from kfp import dsl
from kfp.components import func_to_container_op

@func_to_container_op
def show_results(decision_tree : float, logistic_regression : float, svm : float, naive_bayes : float, xg_boost : float) -> None:
    # Given the outputs from decision_tree, logistic regression, svm, naive_bayes, xg_boost components

    print(f"Decision tree (accuracy): {decision_tree}")
    print(f"Logistic regression (accuracy): {logistic_regression}")
    print(f"SVM (SVC) (accuracy): {svm}")
    print(f"Naive Bayes (Gaussian) (accuracy): {naive_bayes}")
    print(f"XG Boost (accuracy): {xg_boost}")


@dsl.pipeline(name='ML Models Pipeline', description='Applies Decision Tree, Logistic Regression, SVM, Naive Bayes, XG Boost for classification problem.')
def ml_models_pipeline():

    # Loads the yaml manifest for each component
    download = kfp.components.load_component_from_file('download_data/download_data.yaml')
    decision_tree = kfp.components.load_component_from_file('decision_tree/decision_tree.yaml')
    logistic_regression = kfp.components.load_component_from_file('logistic_regression/logistic_regression.yaml')
    svm = kfp.components.load_component_from_file('svm/svm.yaml')
    naive_bayes = kfp.components.load_component_from_file('naive_bayes/naive_bayes.yaml')
    xg_boost = kfp.components.load_component_from_file('xg_boost/xg_boost.yaml')

    # Run download_data task
    download_task = download()

    # Run ML models tasks with input data
    decision_tree_task = decision_tree(download_task.output)
    logistic_regression_task = logistic_regression(download_task.output)
    svm_task = svm(download_task.output)
    naive_bayes_task = naive_bayes(download_task.output)
    xg_boost_task = xg_boost(download_task.output)

    # Given the outputs from ML models tasks
    # the component "show_results" is called to print the results.
    show_results(decision_tree_task.output, logistic_regression_task.output, svm_task.output, naive_bayes_task.output, xg_boost_task.output)



if __name__ == '__main__':
    kfp.compiler.Compiler().compile(ml_models_pipeline, 'MLModelsPipeline.yaml')