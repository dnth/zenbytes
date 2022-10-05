from zenml.pipelines import pipeline


@pipeline(enable_cache=False)
def train_evaluate_deploy_pipeline(
    importer,
    trainer,
    evaluator,
    deployment_trigger,
    model_deployer,
):
    """Train and deploy a model with MLflow."""
    X_train, X_test, y_train, y_test = importer()
    model = trainer(X_train=X_train, y_train=y_train)
    test_acc = evaluator(X_test=X_test, y_test=y_test, model=model)
    deployment_decision = deployment_trigger(test_acc)  # new
    model_deployer(deployment_decision, model)  # new


@pipeline(enable_cache=False)
def continuous_deployment_pipeline(
    importer,
    trainer,
    evaluator,
    get_reference_data,
    drift_detector,
    alerter,
    deployment_trigger,
    model_deployer,
):
    """Links all the steps together in a pipeline"""
    X_train, X_test, y_train, y_test = importer()
    model = trainer(X_train=X_train, y_train=y_train)
    test_acc = evaluator(X_test=X_test, y_test=y_test, model=model)

    reference, comparison = get_reference_data(X_train, X_test)
    drift_report, _ = drift_detector(reference, comparison)

    alerter(drift_report)

    # new
    deployment_decision = deployment_trigger(test_acc)
    model_deployer(deployment_decision, model)
