Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var partition_1 = tslib_1.__importDefault(require("lodash/partition"));
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var locale_1 = require("app/locale");
var dynamicSampling_1 = require("app/types/dynamicSampling");
var withProject_1 = tslib_1.__importDefault(require("app/utils/withProject"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var permissionAlert_1 = tslib_1.__importDefault(require("app/views/settings/organization/permissionAlert"));
var errorRuleModal_1 = tslib_1.__importDefault(require("./modals/errorRuleModal"));
var transactionRuleModal_1 = tslib_1.__importDefault(require("./modals/transactionRuleModal"));
var utils_1 = require("./modals/utils");
var rulesPanel_1 = tslib_1.__importDefault(require("./rulesPanel"));
var utils_2 = require("./utils");
var FiltersAndSampling = /** @class */ (function (_super) {
    tslib_1.__extends(FiltersAndSampling, _super);
    function FiltersAndSampling() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.successfullySubmitted = function (projectDetails, successMessage) {
            _this.setState({ projectDetails: projectDetails });
            if (successMessage) {
                indicator_1.addSuccessMessage(successMessage);
            }
        };
        _this.handleOpenErrorRule = function (rule) { return function () {
            var _a = _this.props, organization = _a.organization, project = _a.project;
            var _b = _this.state, errorRules = _b.errorRules, transactionRules = _b.transactionRules;
            return modal_1.openModal(function (modalProps) { return (<errorRuleModal_1.default {...modalProps} api={_this.api} organization={organization} project={project} rule={rule} errorRules={errorRules} transactionRules={transactionRules} onSubmitSuccess={_this.successfullySubmitted}/>); }, {
                modalCss: utils_1.modalCss,
            });
        }; };
        _this.handleOpenTransactionRule = function (rule) { return function () {
            var _a = _this.props, organization = _a.organization, project = _a.project;
            var _b = _this.state, errorRules = _b.errorRules, transactionRules = _b.transactionRules;
            return modal_1.openModal(function (modalProps) { return (<transactionRuleModal_1.default {...modalProps} api={_this.api} organization={organization} project={project} rule={rule} errorRules={errorRules} transactionRules={transactionRules} onSubmitSuccess={_this.successfullySubmitted}/>); }, {
                modalCss: utils_1.modalCss,
            });
        }; };
        _this.handleAddRule = function (type) {
            return function () {
                if (type === 'errorRules') {
                    _this.handleOpenErrorRule()();
                    return;
                }
                _this.handleOpenTransactionRule()();
            };
        };
        _this.handleEditRule = function (rule) { return function () {
            if (rule.type === dynamicSampling_1.DynamicSamplingRuleType.ERROR) {
                _this.handleOpenErrorRule(rule)();
                return;
            }
            _this.handleOpenTransactionRule(rule)();
        }; };
        _this.handleDeleteRule = function (rule) { return function () {
            var _a = _this.state, errorRules = _a.errorRules, transactionRules = _a.transactionRules;
            var newErrorRules = rule.type === dynamicSampling_1.DynamicSamplingRuleType.ERROR
                ? errorRules.filter(function (errorRule) { return errorRule.id !== rule.id; })
                : errorRules;
            var newTransactionRules = rule.type !== dynamicSampling_1.DynamicSamplingRuleType.ERROR
                ? transactionRules.filter(function (transactionRule) { return transactionRule.id !== rule.id; })
                : transactionRules;
            var newRules = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(newErrorRules)), tslib_1.__read(newTransactionRules));
            _this.submitRules(newRules, locale_1.t('Successfully deleted dynamic sampling rule'), locale_1.t('An error occurred while deleting dynamic sampling rule'));
        }; };
        _this.handleUpdateRules = function (rules) {
            var _a;
            if (!rules.length) {
                return;
            }
            var _b = _this.state, errorRules = _b.errorRules, transactionRules = _b.transactionRules;
            if (((_a = rules[0]) === null || _a === void 0 ? void 0 : _a.type) === dynamicSampling_1.DynamicSamplingRuleType.ERROR) {
                _this.submitRules(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(rules)), tslib_1.__read(transactionRules)));
                return;
            }
            _this.submitRules(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(errorRules)), tslib_1.__read(rules)));
        };
        return _this;
    }
    FiltersAndSampling.prototype.getTitle = function () {
        return locale_1.t('Filters & Sampling');
    };
    FiltersAndSampling.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { errorRules: [], transactionRules: [], projectDetails: null });
    };
    FiltersAndSampling.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        return [['projectDetails', "/projects/" + organization.slug + "/" + project.slug + "/"]];
    };
    FiltersAndSampling.prototype.componentDidMount = function () {
        this.getRules();
    };
    FiltersAndSampling.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (prevState.projectDetails !== this.state.projectDetails) {
            this.getRules();
            return;
        }
    };
    FiltersAndSampling.prototype.getRules = function () {
        var _a;
        var projectDetails = this.state.projectDetails;
        if (!projectDetails) {
            return;
        }
        var dynamicSampling = projectDetails.dynamicSampling;
        var rules = (_a = dynamicSampling === null || dynamicSampling === void 0 ? void 0 : dynamicSampling.rules) !== null && _a !== void 0 ? _a : [];
        var _b = tslib_1.__read(partition_1.default(rules, function (rule) { return rule.type === dynamicSampling_1.DynamicSamplingRuleType.ERROR; }), 2), errorRules = _b[0], transactionRules = _b[1];
        this.setState({ errorRules: errorRules, transactionRules: transactionRules });
    };
    FiltersAndSampling.prototype.submitRules = function (newRules, successMessage, errorMessage) {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, organization, project, projectDetails, error_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, project = _a.project;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/", { method: 'PUT', data: { dynamicSampling: { rules: newRules } } })];
                    case 2:
                        projectDetails = _b.sent();
                        this.successfullySubmitted(projectDetails, successMessage);
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.getRules();
                        if (errorMessage) {
                            indicator_1.addErrorMessage(errorMessage);
                        }
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    FiltersAndSampling.prototype.renderBody = function () {
        var _a = this.state, errorRules = _a.errorRules, transactionRules = _a.transactionRules;
        var hasAccess = this.props.hasAccess;
        var disabled = !hasAccess;
        var hasNotSupportedConditionOperator = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(errorRules)), tslib_1.__read(transactionRules)).some(function (rule) { return rule.condition.op !== dynamicSampling_1.DynamicSamplingConditionOperator.AND; });
        if (hasNotSupportedConditionOperator) {
            return (<alert_1.default type="error">
          {locale_1.t('A condition operator has been found that is not yet supported.')}
        </alert_1.default>);
        }
        return (<React.Fragment>
        <settingsPageHeader_1.default title={this.getTitle()}/>
        <permissionAlert_1.default />
        <textBlock_1.default>
          {locale_1.tct('Manage the inbound data you want to store. To change the sampling rate or rate limits, [link:update your SDK configuration]. The rules added below will apply on top of your SDK configuration. Any new rule may take a few minutes to propagate.', {
                link: <externalLink_1.default href={utils_2.DYNAMIC_SAMPLING_DOC_LINK}/>,
            })}
        </textBlock_1.default>
        <rulesPanel_1.default rules={errorRules} disabled={disabled} onAddRule={this.handleAddRule('errorRules')} onEditRule={this.handleEditRule} onDeleteRule={this.handleDeleteRule} onUpdateRules={this.handleUpdateRules} isErrorPanel/>
        <textBlock_1.default>
          {locale_1.t('Rules for traces should precede rules for individual transactions.')}
        </textBlock_1.default>
        <rulesPanel_1.default rules={transactionRules} disabled={disabled} onAddRule={this.handleAddRule('transactionRules')} onEditRule={this.handleEditRule} onDeleteRule={this.handleDeleteRule} onUpdateRules={this.handleUpdateRules}/>
      </React.Fragment>);
    };
    return FiltersAndSampling;
}(asyncView_1.default));
exports.default = withProject_1.default(FiltersAndSampling);
//# sourceMappingURL=filtersAndSampling.jsx.map