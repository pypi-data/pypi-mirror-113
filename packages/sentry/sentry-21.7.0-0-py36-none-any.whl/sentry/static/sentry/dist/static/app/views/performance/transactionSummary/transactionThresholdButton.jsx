Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var transactionThresholdModal_1 = tslib_1.__importStar(require("./transactionThresholdModal"));
var TransactionThresholdButton = /** @class */ (function (_super) {
    tslib_1.__extends(TransactionThresholdButton, _super);
    function TransactionThresholdButton() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            transactionThreshold: undefined,
            transactionThresholdMetric: undefined,
            loadingThreshold: false,
        };
        _this.fetchTransactionThreshold = function () {
            var _a = _this.props, api = _a.api, organization = _a.organization, transactionName = _a.transactionName;
            var project = _this.getProject();
            if (!utils_1.defined(project)) {
                return;
            }
            var transactionThresholdUrl = "/organizations/" + organization.slug + "/project-transaction-threshold-override/";
            _this.setState({ loadingThreshold: true });
            api
                .requestPromise(transactionThresholdUrl, {
                method: 'GET',
                includeAllArgs: true,
                query: {
                    project: project.id,
                    transaction: transactionName,
                },
            })
                .then(function (_a) {
                var _b = tslib_1.__read(_a, 1), data = _b[0];
                _this.setState({
                    loadingThreshold: false,
                    transactionThreshold: data.threshold,
                    transactionThresholdMetric: data.metric,
                });
            })
                .catch(function () {
                var projectThresholdUrl = "/projects/" + organization.slug + "/" + project.slug + "/transaction-threshold/configure/";
                _this.props.api
                    .requestPromise(projectThresholdUrl, {
                    method: 'GET',
                    includeAllArgs: true,
                    query: {
                        project: project.id,
                    },
                })
                    .then(function (_a) {
                    var _b = tslib_1.__read(_a, 1), data = _b[0];
                    _this.setState({
                        loadingThreshold: false,
                        transactionThreshold: data.threshold,
                        transactionThresholdMetric: data.metric,
                    });
                })
                    .catch(function (err) {
                    var _a, _b;
                    _this.setState({ loadingThreshold: false });
                    var errorMessage = (_b = (_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.threshold) !== null && _b !== void 0 ? _b : null;
                    indicator_1.addErrorMessage(errorMessage);
                });
            });
        };
        return _this;
    }
    TransactionThresholdButton.prototype.componentDidMount = function () {
        this.fetchTransactionThreshold();
    };
    TransactionThresholdButton.prototype.getProject = function () {
        var _a = this.props, projects = _a.projects, eventView = _a.eventView;
        if (!utils_1.defined(eventView)) {
            return undefined;
        }
        var projectId = String(eventView.project[0]);
        var project = projects.find(function (proj) { return proj.id === projectId; });
        return project;
    };
    TransactionThresholdButton.prototype.onChangeThreshold = function (threshold, metric) {
        var onChangeThreshold = this.props.onChangeThreshold;
        this.setState({
            transactionThreshold: threshold,
            transactionThresholdMetric: metric,
        });
        if (utils_1.defined(onChangeThreshold)) {
            onChangeThreshold(threshold, metric);
        }
    };
    TransactionThresholdButton.prototype.openModal = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, transactionName = _a.transactionName, eventView = _a.eventView;
        var _b = this.state, transactionThreshold = _b.transactionThreshold, transactionThresholdMetric = _b.transactionThresholdMetric;
        modal_1.openModal(function (modalProps) { return (<transactionThresholdModal_1.default {...modalProps} organization={organization} transactionName={transactionName} eventView={eventView} transactionThreshold={transactionThreshold} transactionThresholdMetric={transactionThresholdMetric} onApply={function (threshold, metric) { return _this.onChangeThreshold(threshold, metric); }}/>); }, { modalCss: transactionThresholdModal_1.modalCss, backdrop: 'static' });
    };
    TransactionThresholdButton.prototype.render = function () {
        var _this = this;
        var loadingThreshold = this.state.loadingThreshold;
        return (<button_1.default onClick={function () { return _this.openModal(); }} icon={<icons_1.IconSettings />} disabled={loadingThreshold} aria-label={locale_1.t('Settings')} data-test-id="set-transaction-threshold"/>);
    };
    return TransactionThresholdButton;
}(react_1.Component));
exports.default = withApi_1.default(withProjects_1.default(TransactionThresholdButton));
//# sourceMappingURL=transactionThresholdButton.jsx.map