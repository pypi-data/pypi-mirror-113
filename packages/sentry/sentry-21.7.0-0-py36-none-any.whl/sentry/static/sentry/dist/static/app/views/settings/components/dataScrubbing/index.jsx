Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var api_1 = require("app/api");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var add_1 = tslib_1.__importDefault(require("./modals/add"));
var edit_1 = tslib_1.__importDefault(require("./modals/edit"));
var content_1 = tslib_1.__importDefault(require("./content"));
var convertRelayPiiConfig_1 = tslib_1.__importDefault(require("./convertRelayPiiConfig"));
var organizationRules_1 = tslib_1.__importDefault(require("./organizationRules"));
var submitRules_1 = tslib_1.__importDefault(require("./submitRules"));
var ADVANCED_DATASCRUBBING_LINK = 'https://docs.sentry.io/product/data-management-settings/scrubbing/advanced-datascrubbing/';
var DataScrubbing = /** @class */ (function (_super) {
    tslib_1.__extends(DataScrubbing, _super);
    function DataScrubbing() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            rules: [],
            savedRules: [],
            relayPiiConfig: _this.props.relayPiiConfig,
            orgRules: [],
        };
        _this.api = new api_1.Client();
        _this.handleOpenAddModal = function () {
            var rules = _this.state.rules;
            modal_1.openModal(function (modalProps) { return (<add_1.default {...modalProps} projectId={_this.props.projectId} savedRules={rules} api={_this.api} endpoint={_this.props.endpoint} orgSlug={_this.props.organization.slug} onSubmitSuccess={function (response) {
                    _this.successfullySaved(response, locale_1.t('Successfully added data scrubbing rule'));
                }}/>); });
        };
        _this.handleOpenEditModal = function (id) { return function () {
            var rules = _this.state.rules;
            modal_1.openModal(function (modalProps) { return (<edit_1.default {...modalProps} rule={rules[id]} projectId={_this.props.projectId} savedRules={rules} api={_this.api} endpoint={_this.props.endpoint} orgSlug={_this.props.organization.slug} onSubmitSuccess={function (response) {
                    _this.successfullySaved(response, locale_1.t('Successfully updated data scrubbing rule'));
                }}/>); });
        }; };
        _this.handleDelete = function (id) { return function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var rules, filteredRules, data, convertedRules, _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        rules = this.state.rules;
                        filteredRules = rules.filter(function (rule) { return rule.id !== id; });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, submitRules_1.default(this.api, this.props.endpoint, filteredRules)];
                    case 2:
                        data = _b.sent();
                        if (data === null || data === void 0 ? void 0 : data.relayPiiConfig) {
                            convertedRules = convertRelayPiiConfig_1.default(data.relayPiiConfig);
                            this.setState({ rules: convertedRules });
                            indicator_1.addSuccessMessage(locale_1.t('Successfully deleted data scrubbing rule'));
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        indicator_1.addErrorMessage(locale_1.t('An unknown error occurred while deleting data scrubbing rule'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); }; };
        return _this;
    }
    DataScrubbing.prototype.componentDidMount = function () {
        this.loadRules();
        this.loadOrganizationRules();
    };
    DataScrubbing.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (prevState.relayPiiConfig !== this.state.relayPiiConfig) {
            this.loadRules();
        }
    };
    DataScrubbing.prototype.componentWillUnmount = function () {
        this.api.clear();
    };
    DataScrubbing.prototype.loadOrganizationRules = function () {
        var _a = this.props, organization = _a.organization, projectId = _a.projectId;
        if (projectId) {
            try {
                this.setState({
                    orgRules: convertRelayPiiConfig_1.default(organization.relayPiiConfig),
                });
            }
            catch (_b) {
                indicator_1.addErrorMessage(locale_1.t('Unable to load organization rules'));
            }
        }
    };
    DataScrubbing.prototype.loadRules = function () {
        try {
            var convertedRules = convertRelayPiiConfig_1.default(this.state.relayPiiConfig);
            this.setState({
                rules: convertedRules,
                savedRules: convertedRules,
            });
        }
        catch (_a) {
            indicator_1.addErrorMessage(locale_1.t('Unable to load project rules'));
        }
    };
    DataScrubbing.prototype.successfullySaved = function (response, successMessage) {
        var onSubmitSuccess = this.props.onSubmitSuccess;
        this.setState({ rules: convertRelayPiiConfig_1.default(response.relayPiiConfig) });
        indicator_1.addSuccessMessage(successMessage);
        onSubmitSuccess === null || onSubmitSuccess === void 0 ? void 0 : onSubmitSuccess(response);
    };
    DataScrubbing.prototype.render = function () {
        var _a = this.props, additionalContext = _a.additionalContext, disabled = _a.disabled, projectId = _a.projectId;
        var _b = this.state, orgRules = _b.orgRules, rules = _b.rules;
        return (<React.Fragment>
        <panels_1.Panel data-test-id="advanced-data-scrubbing">
          <panels_1.PanelHeader>
            <div>{locale_1.t('Advanced Data Scrubbing')}</div>
          </panels_1.PanelHeader>
          <panels_1.PanelAlert type="info">
            {additionalContext}{' '}
            {"" + locale_1.t('The new rules will only apply to upcoming events. ')}{' '}
            {locale_1.tct('For more details, see [linkToDocs].', {
                linkToDocs: (<externalLink_1.default href={ADVANCED_DATASCRUBBING_LINK}>
                  {locale_1.t('full documentation on data scrubbing')}
                </externalLink_1.default>),
            })}
          </panels_1.PanelAlert>
          <panels_1.PanelBody>
            {projectId && <organizationRules_1.default rules={orgRules}/>}
            <content_1.default rules={rules} onDeleteRule={this.handleDelete} onEditRule={this.handleOpenEditModal} disabled={disabled}/>
            <PanelAction>
              <button_1.default href={ADVANCED_DATASCRUBBING_LINK} target="_blank">
                {locale_1.t('Read the docs')}
              </button_1.default>
              <button_1.default disabled={disabled} onClick={this.handleOpenAddModal} priority="primary">
                {locale_1.t('Add Rule')}
              </button_1.default>
            </PanelAction>
          </panels_1.PanelBody>
        </panels_1.Panel>
      </React.Fragment>);
    };
    return DataScrubbing;
}(React.Component));
exports.default = DataScrubbing;
var PanelAction = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", ";\n  position: relative;\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto auto;\n  justify-content: flex-end;\n  border-top: 1px solid ", ";\n"], ["\n  padding: ", " ", ";\n  position: relative;\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto auto;\n  justify-content: flex-end;\n  border-top: 1px solid ", ";\n"])), space_1.default(1), space_1.default(2), space_1.default(1), function (p) { return p.theme.border; });
var templateObject_1;
//# sourceMappingURL=index.jsx.map