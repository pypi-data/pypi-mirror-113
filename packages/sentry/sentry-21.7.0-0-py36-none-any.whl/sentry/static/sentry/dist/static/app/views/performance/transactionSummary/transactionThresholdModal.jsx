Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = exports.METRIC_CHOICES = exports.TransactionThresholdMetric = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var cloneDeep_1 = tslib_1.__importDefault(require("lodash/cloneDeep"));
var set_1 = tslib_1.__importDefault(require("lodash/set"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var featureBadge_1 = tslib_1.__importDefault(require("app/components/featureBadge"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var utils_2 = require("./utils");
var TransactionThresholdMetric;
(function (TransactionThresholdMetric) {
    TransactionThresholdMetric["TRANSACTION_DURATION"] = "duration";
    TransactionThresholdMetric["LARGEST_CONTENTFUL_PAINT"] = "lcp";
})(TransactionThresholdMetric = exports.TransactionThresholdMetric || (exports.TransactionThresholdMetric = {}));
exports.METRIC_CHOICES = [
    { label: locale_1.t('Transaction Duration'), value: 'duration' },
    { label: locale_1.t('Largest Contentful Paint'), value: 'lcp' },
];
var TransactionThresholdModal = /** @class */ (function (_super) {
    tslib_1.__extends(TransactionThresholdModal, _super);
    function TransactionThresholdModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            threshold: _this.props.transactionThreshold,
            metric: _this.props.transactionThresholdMetric,
            error: null,
        };
        _this.handleApply = function (event) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, closeModal, organization, transactionName, onApply, project, transactionThresholdUrl;
            var _this = this;
            return tslib_1.__generator(this, function (_b) {
                event.preventDefault();
                _a = this.props, api = _a.api, closeModal = _a.closeModal, organization = _a.organization, transactionName = _a.transactionName, onApply = _a.onApply;
                project = this.getProject();
                if (!utils_1.defined(project)) {
                    return [2 /*return*/];
                }
                transactionThresholdUrl = "/organizations/" + organization.slug + "/project-transaction-threshold-override/";
                api
                    .requestPromise(transactionThresholdUrl, {
                    method: 'POST',
                    includeAllArgs: true,
                    query: {
                        project: project.id,
                    },
                    data: {
                        transaction: transactionName,
                        threshold: this.state.threshold,
                        metric: this.state.metric,
                    },
                })
                    .then(function () {
                    closeModal();
                    if (onApply) {
                        onApply(_this.state.threshold, _this.state.metric);
                    }
                })
                    .catch(function (err) {
                    var _a, _b, _c, _d;
                    _this.setState({
                        error: err,
                    });
                    var errorMessage = (_d = (_b = (_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.threshold) !== null && _b !== void 0 ? _b : (_c = err.responseJSON) === null || _c === void 0 ? void 0 : _c.non_field_errors) !== null && _d !== void 0 ? _d : null;
                    indicator_1.addErrorMessage(errorMessage);
                });
                return [2 /*return*/];
            });
        }); };
        _this.handleFieldChange = function (field) { return function (value) {
            _this.setState(function (prevState) {
                var newState = cloneDeep_1.default(prevState);
                set_1.default(newState, field, value);
                return tslib_1.__assign(tslib_1.__assign({}, newState), { errors: undefined });
            });
        }; };
        _this.handleReset = function (event) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, closeModal, organization, transactionName, onApply, project, transactionThresholdUrl;
            var _this = this;
            return tslib_1.__generator(this, function (_b) {
                event.preventDefault();
                _a = this.props, api = _a.api, closeModal = _a.closeModal, organization = _a.organization, transactionName = _a.transactionName, onApply = _a.onApply;
                project = this.getProject();
                if (!utils_1.defined(project)) {
                    return [2 /*return*/];
                }
                transactionThresholdUrl = "/organizations/" + organization.slug + "/project-transaction-threshold-override/";
                api
                    .requestPromise(transactionThresholdUrl, {
                    method: 'DELETE',
                    includeAllArgs: true,
                    query: {
                        project: project.id,
                    },
                    data: {
                        transaction: transactionName,
                    },
                })
                    .then(function () {
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
                            threshold: data.threshold,
                            metric: data.metric,
                        });
                        closeModal();
                        if (onApply) {
                            onApply(_this.state.threshold, _this.state.metric);
                        }
                    })
                        .catch(function (err) {
                        var _a, _b;
                        var errorMessage = (_b = (_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.threshold) !== null && _b !== void 0 ? _b : null;
                        indicator_1.addErrorMessage(errorMessage);
                    });
                })
                    .catch(function (err) {
                    _this.setState({
                        error: err,
                    });
                });
                return [2 /*return*/];
            });
        }); };
        return _this;
    }
    TransactionThresholdModal.prototype.getProject = function () {
        var _a = this.props, projects = _a.projects, eventView = _a.eventView, project = _a.project;
        if (utils_1.defined(project)) {
            return projects.find(function (proj) { return proj.id === project; });
        }
        else {
            var projectId_1 = String(eventView.project[0]);
            return projects.find(function (proj) { return proj.id === projectId_1; });
        }
    };
    TransactionThresholdModal.prototype.renderModalFields = function () {
        var _this = this;
        return (<React.Fragment>
        <field_1.default data-test-id="response-metric" label={locale_1.t('Calculation Method')} inline={false} help={locale_1.t('This determines which duration metric is used for the Response Time Threshold.')} showHelpInTooltip flexibleControlStateSize stacked required>
          <selectControl_1.default required options={exports.METRIC_CHOICES.slice()} name="responseMetric" label={locale_1.t('Calculation Method')} value={this.state.metric} onChange={function (option) {
                _this.handleFieldChange('metric')(option.value);
            }}/>
        </field_1.default>
        <field_1.default data-test-id="response-time-threshold" label={locale_1.t('Response Time Threshold (ms)')} inline={false} help={locale_1.t('The satisfactory response time for the calculation method defined above. This is used to calculate Apdex and User Misery scores.')} showHelpInTooltip flexibleControlStateSize stacked required>
          <input_1.default type="number" name="threshold" required pattern="[0-9]*(\.[0-9]*)?" onChange={function (event) {
                _this.handleFieldChange('threshold')(event.target.value);
            }} value={this.state.threshold} step={100} min={100}/>
        </field_1.default>
      </React.Fragment>);
    };
    TransactionThresholdModal.prototype.render = function () {
        var _a = this.props, Header = _a.Header, Body = _a.Body, Footer = _a.Footer, organization = _a.organization, transactionName = _a.transactionName, eventView = _a.eventView;
        var project = this.getProject();
        var summaryView = eventView.clone();
        summaryView.query = summaryView.getQueryWithAdditionalConditions();
        var target = utils_2.transactionSummaryRouteWithQuery({
            orgSlug: organization.slug,
            transaction: transactionName,
            query: summaryView.generateQueryStringObject(),
            projectID: project === null || project === void 0 ? void 0 : project.id,
        });
        return (<React.Fragment>
        <Header closeButton>
          <h4>
            {locale_1.t('Transaction Settings')} <featureBadge_1.default type="beta"/>
          </h4>
        </Header>
        <Body>
          <Instruction>
            {locale_1.tct('The changes below will only be applied to [transaction]. To set it at a more global level, go to [projectSettings: Project Settings].', {
                transaction: <react_router_1.Link to={target}>{transactionName}</react_router_1.Link>,
                projectSettings: (<react_router_1.Link to={"/settings/" + organization.slug + "/projects/" + (project === null || project === void 0 ? void 0 : project.slug) + "/performance/"}/>),
            })}
          </Instruction>
          {this.renderModalFields()}
        </Body>
        <Footer>
          <buttonBar_1.default gap={1}>
            <button_1.default priority="default" onClick={this.handleReset} data-test-id="reset-all">
              {locale_1.t('Reset All')}
            </button_1.default>
            <button_1.default label={locale_1.t('Apply')} priority="primary" onClick={this.handleApply} data-test-id="apply-threshold">
              {locale_1.t('Apply')}
            </button_1.default>
          </buttonBar_1.default>
        </Footer>
      </React.Fragment>);
    };
    return TransactionThresholdModal;
}(React.Component));
var Instruction = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(4));
exports.modalCss = react_1.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  max-width: 650px;\n  margin: 70px auto;\n"], ["\n  width: 100%;\n  max-width: 650px;\n  margin: 70px auto;\n"])));
exports.default = withApi_1.default(withProjects_1.default(TransactionThresholdModal));
var templateObject_1, templateObject_2;
//# sourceMappingURL=transactionThresholdModal.jsx.map