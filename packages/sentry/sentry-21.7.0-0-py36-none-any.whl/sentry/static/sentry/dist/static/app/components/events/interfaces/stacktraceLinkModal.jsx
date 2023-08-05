Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var integrationUtil_1 = require("app/utils/integrationUtil");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var inputField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/inputField"));
var StacktraceLinkModal = /** @class */ (function (_super) {
    tslib_1.__extends(StacktraceLinkModal, _super);
    function StacktraceLinkModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            sourceCodeInput: '',
        };
        _this.handleSubmit = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var sourceCodeInput, _a, api, closeModal, filename, onSubmit, organization, project, parsingEndpoint, configData, configEndpoint, err_1, errors, apiErrors;
            var _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        sourceCodeInput = this.state.sourceCodeInput;
                        _a = this.props, api = _a.api, closeModal = _a.closeModal, filename = _a.filename, onSubmit = _a.onSubmit, organization = _a.organization, project = _a.project;
                        integrationUtil_1.trackIntegrationEvent('integrations.stacktrace_submit_config', {
                            setup_type: 'automatic',
                            view: 'stacktrace_issue_details',
                        }, organization);
                        parsingEndpoint = "/projects/" + organization.slug + "/" + project.slug + "/repo-path-parsing/";
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 4, , 5]);
                        return [4 /*yield*/, api.requestPromise(parsingEndpoint, {
                                method: 'POST',
                                data: {
                                    sourceUrl: sourceCodeInput,
                                    stackPath: filename,
                                },
                            })];
                    case 2:
                        configData = _c.sent();
                        configEndpoint = "/organizations/" + organization.slug + "/code-mappings/";
                        return [4 /*yield*/, api.requestPromise(configEndpoint, {
                                method: 'POST',
                                data: tslib_1.__assign(tslib_1.__assign({}, configData), { projectId: project.id, integrationId: configData.integrationId }),
                            })];
                    case 3:
                        _c.sent();
                        indicator_1.addSuccessMessage(locale_1.t('Stack trace configuration saved.'));
                        integrationUtil_1.trackIntegrationEvent('integrations.stacktrace_complete_setup', {
                            setup_type: 'automatic',
                            provider: (_b = configData.config) === null || _b === void 0 ? void 0 : _b.provider.key,
                            view: 'stacktrace_issue_details',
                        }, organization);
                        closeModal();
                        onSubmit();
                        return [3 /*break*/, 5];
                    case 4:
                        err_1 = _c.sent();
                        errors = (err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON)
                            ? Array.isArray(err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON)
                                ? err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON
                                : Object.values(err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON)
                            : [];
                        apiErrors = errors.length > 0 ? ": " + errors.join(', ') : '';
                        indicator_1.addErrorMessage(locale_1.t('Something went wrong%s', apiErrors));
                        return [3 /*break*/, 5];
                    case 5: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    StacktraceLinkModal.prototype.onHandleChange = function (sourceCodeInput) {
        this.setState({
            sourceCodeInput: sourceCodeInput,
        });
    };
    StacktraceLinkModal.prototype.onManualSetup = function (provider) {
        integrationUtil_1.trackIntegrationEvent('integrations.stacktrace_manual_option_clicked', {
            view: 'stacktrace_issue_details',
            setup_type: 'manual',
            provider: provider,
        }, this.props.organization);
    };
    StacktraceLinkModal.prototype.render = function () {
        var _this = this;
        var sourceCodeInput = this.state.sourceCodeInput;
        var _a = this.props, Header = _a.Header, Body = _a.Body, filename = _a.filename, integrations = _a.integrations, organization = _a.organization;
        var baseUrl = "/settings/" + organization.slug + "/integrations";
        return (<react_1.Fragment>
        <Header closeButton>{locale_1.t('Link Stack Trace To Source Code')}</Header>
        <Body>
          <ModalContainer>
            <div>
              <h6>{locale_1.t('Automatic Setup')}</h6>
              {locale_1.tct('Enter the source code URL corresponding to stack trace filename [filename] so we can automatically set up stack trace linking for this project.', {
                filename: <code>{filename}</code>,
            })}
            </div>
            <SourceCodeInput>
              <StyledInputField inline={false} flexibleControlStateSize stacked name="source-code-input" type="text" value={sourceCodeInput} onChange={function (val) { return _this.onHandleChange(val); }} placeholder={locale_1.t("https://github.com/helloworld/Hello-World/blob/master/" + filename)}/>
              <buttonBar_1.default>
                <button_1.default data-test-id="quick-setup-button" type="button" onClick={function () { return _this.handleSubmit(); }}>
                  {locale_1.t('Submit')}
                </button_1.default>
              </buttonBar_1.default>
            </SourceCodeInput>
            <div>
              <h6>{locale_1.t('Manual Setup')}</h6>
              <alert_1.default type="warning">
                {locale_1.t('We recommend this for more complicated configurations, like projects with multiple repositories.')}
              </alert_1.default>
              {locale_1.t("To manually configure stack trace linking, select the integration you'd like to use for mapping:")}
            </div>
            <ManualSetup>
              {integrations.map(function (integration) { return (<button_1.default key={integration.id} type="button" onClick={function () { return _this.onManualSetup(integration.provider.key); }} to={baseUrl + "/" + integration.provider.key + "/" + integration.id + "/?tab=codeMappings&referrer=stacktrace-issue-details"}>
                  {integrationUtil_1.getIntegrationIcon(integration.provider.key)}
                  <IntegrationName>{integration.name}</IntegrationName>
                </button_1.default>); })}
            </ManualSetup>
            <FeedbackAlert type="info" icon={<icons_1.IconInfo />}>
              {locale_1.tct('Got feedback? Email [email:ecosystem-feedback@sentry.io].', {
                email: <a href="mailto:ecosystem-feedback@sentry.io"/>,
            })}
            </FeedbackAlert>
          </ModalContainer>
        </Body>
      </react_1.Fragment>);
    };
    return StacktraceLinkModal;
}(react_1.Component));
var SourceCodeInput = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 5fr 1fr;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 5fr 1fr;\n  grid-gap: ", ";\n"])), space_1.default(1));
var ManualSetup = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  justify-items: center;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  justify-items: center;\n"])), space_1.default(1));
var ModalContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n\n  code {\n    word-break: break-word;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n\n  code {\n    word-break: break-word;\n  }\n"])), space_1.default(3));
var FeedbackAlert = styled_1.default(alert_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin: 20px 0px 0px 0px;\n"], ["\n  margin: 20px 0px 0px 0px;\n"])));
var StyledInputField = styled_1.default(inputField_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  padding: 0px;\n"], ["\n  padding: 0px;\n"])));
var IntegrationName = styled_1.default('p')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  padding-left: 10px;\n"], ["\n  padding-left: 10px;\n"])));
exports.default = withApi_1.default(StacktraceLinkModal);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=stacktraceLinkModal.jsx.map