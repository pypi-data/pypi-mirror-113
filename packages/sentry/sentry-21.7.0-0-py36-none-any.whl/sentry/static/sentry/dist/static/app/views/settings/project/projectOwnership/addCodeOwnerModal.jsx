Object.defineProperty(exports, "__esModule", { value: true });
exports.AddCodeOwnerModal = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var integrationUtil_1 = require("app/utils/integrationUtil");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var selectField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/selectField"));
var AddCodeOwnerModal = /** @class */ (function (_super) {
    tslib_1.__extends(AddCodeOwnerModal, _super);
    function AddCodeOwnerModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            codeownerFile: null,
            codeMappingId: null,
            isLoading: false,
            error: false,
            errorJSON: null,
        };
        _this.fetchFile = function (codeMappingId) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var organization, data, _err_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        organization = this.props.organization;
                        this.setState({
                            codeMappingId: codeMappingId,
                            codeownerFile: null,
                            error: false,
                            errorJSON: null,
                            isLoading: true,
                        });
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.props.api.requestPromise("/organizations/" + organization.slug + "/code-mappings/" + codeMappingId + "/codeowners/", {
                                method: 'GET',
                            })];
                    case 2:
                        data = _a.sent();
                        this.setState({ codeownerFile: data, isLoading: false });
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        this.setState({ isLoading: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.addFile = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, organization, project, codeMappings, _b, codeownerFile, codeMappingId, postData, data, codeMapping, err_1;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, project = _a.project, codeMappings = _a.codeMappings;
                        _b = this.state, codeownerFile = _b.codeownerFile, codeMappingId = _b.codeMappingId;
                        if (!codeownerFile) return [3 /*break*/, 4];
                        postData = {
                            codeMappingId: codeMappingId,
                            raw: codeownerFile.raw,
                        };
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.props.api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/codeowners/", {
                                method: 'POST',
                                data: postData,
                            })];
                    case 2:
                        data = _c.sent();
                        codeMapping = codeMappings.find(function (mapping) { return mapping.id === (codeMappingId === null || codeMappingId === void 0 ? void 0 : codeMappingId.toString()); });
                        this.handleAddedFile(tslib_1.__assign(tslib_1.__assign({}, data), { codeMapping: codeMapping }));
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _c.sent();
                        if (err_1.responseJSON.raw) {
                            this.setState({ error: true, errorJSON: err_1.responseJSON, isLoading: false });
                        }
                        else {
                            indicator_1.addErrorMessage(locale_1.t(Object.values(err_1.responseJSON).flat().join(' ')));
                        }
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AddCodeOwnerModal.prototype.handleAddedFile = function (data) {
        this.props.onSave(data);
        this.props.closeModal();
    };
    AddCodeOwnerModal.prototype.sourceFile = function (codeownerFile) {
        return (<panels_1.Panel>
        <SourceFileBody>
          <icons_1.IconCheckmark size="md" isCircled color="green200"/>
          {codeownerFile.filepath}
          <button_1.default size="small" href={codeownerFile.html_url} target="_blank">
            {locale_1.t('Preview File')}
          </button_1.default>
        </SourceFileBody>
      </panels_1.Panel>);
    };
    AddCodeOwnerModal.prototype.errorMessage = function (baseUrl) {
        var _a;
        var _b = this.state, errorJSON = _b.errorJSON, codeMappingId = _b.codeMappingId;
        var codeMappings = this.props.codeMappings;
        var codeMapping = codeMappings.find(function (mapping) { return mapping.id === codeMappingId; });
        var _c = codeMapping, integrationId = _c.integrationId, provider = _c.provider;
        var errActors = (_a = errorJSON === null || errorJSON === void 0 ? void 0 : errorJSON.raw) === null || _a === void 0 ? void 0 : _a[0].split('\n').map(function (el) { return <p>{el}</p>; });
        return (<alert_1.default type="error" icon={<icons_1.IconNot size="md"/>}>
        {errActors}
        {codeMapping && (<p>
            {locale_1.tct('Configure [userMappingsLink:User Mappings] or [teamMappingsLink:Team Mappings] for any missing associations.', {
                    userMappingsLink: (<link_1.default to={baseUrl + "/" + (provider === null || provider === void 0 ? void 0 : provider.key) + "/" + integrationId + "/?tab=userMappings&referrer=add-codeowners"}/>),
                    teamMappingsLink: (<link_1.default to={baseUrl + "/" + (provider === null || provider === void 0 ? void 0 : provider.key) + "/" + integrationId + "/?tab=teamMappings&referrer=add-codeowners"}/>),
                })}
          </p>)}
        {locale_1.tct('[addAndSkip:Add and Skip Missing Associations] will add your codeowner file and skip any rules that having missing associations. You can add associations later for any skipped rules.', { addAndSkip: <strong>Add and Skip Missing Associations</strong> })}
      </alert_1.default>);
    };
    AddCodeOwnerModal.prototype.noSourceFile = function () {
        var _a = this.state, codeMappingId = _a.codeMappingId, isLoading = _a.isLoading;
        if (isLoading) {
            return (<Container>
          <loadingIndicator_1.default mini/>
        </Container>);
        }
        if (!codeMappingId) {
            return null;
        }
        return (<panels_1.Panel>
        <NoSourceFileBody>
          {codeMappingId ? (<react_1.Fragment>
              <icons_1.IconNot size="md" color="red200"/>
              {locale_1.t('No codeowner file found.')}
            </react_1.Fragment>) : null}
        </NoSourceFileBody>
      </panels_1.Panel>);
    };
    AddCodeOwnerModal.prototype.render = function () {
        var _a = this.props, Header = _a.Header, Body = _a.Body, Footer = _a.Footer;
        var _b = this.state, codeownerFile = _b.codeownerFile, error = _b.error, errorJSON = _b.errorJSON;
        var _c = this.props, codeMappings = _c.codeMappings, integrations = _c.integrations, organization = _c.organization;
        var baseUrl = "/settings/" + organization.slug + "/integrations";
        return (<react_1.Fragment>
        <Header closeButton>{locale_1.t('Add Code Owner File')}</Header>
        <Body>
          {!codeMappings.length && (<react_1.Fragment>
              <div>
                {locale_1.t("Configure code mapping to add your CODEOWNERS file. Select the integration you'd like to use for mapping:")}
              </div>
              <IntegrationsList>
                {integrations.map(function (integration) { return (<button_1.default key={integration.id} type="button" to={baseUrl + "/" + integration.provider.key + "/" + integration.id + "/?tab=codeMappings&referrer=add-codeowners"}>
                    {integrationUtil_1.getIntegrationIcon(integration.provider.key)}
                    <IntegrationName>{integration.name}</IntegrationName>
                  </button_1.default>); })}
              </IntegrationsList>
            </react_1.Fragment>)}
          {codeMappings.length > 0 && (<form_1.default apiMethod="POST" apiEndpoint="/code-mappings/" hideFooter initialData={{}}>
              <StyledSelectField name="codeMappingId" label={locale_1.t('Apply an existing code mapping')} choices={codeMappings.map(function (cm) { return [
                    cm.id,
                    cm.repoName,
                ]; })} onChange={this.fetchFile} required inline={false} flexibleControlStateSize stacked/>

              <FileResult>
                {codeownerFile ? this.sourceFile(codeownerFile) : this.noSourceFile()}
                {error && errorJSON && this.errorMessage(baseUrl)}
              </FileResult>
            </form_1.default>)}
        </Body>
        <Footer>
          <button_1.default disabled={codeownerFile ? false : true} label={locale_1.t('Add File')} priority="primary" onClick={this.addFile}>
            {locale_1.t('Add File')}
          </button_1.default>
        </Footer>
      </react_1.Fragment>);
    };
    return AddCodeOwnerModal;
}(react_1.Component));
exports.AddCodeOwnerModal = AddCodeOwnerModal;
exports.default = withApi_1.default(AddCodeOwnerModal);
var StyledSelectField = styled_1.default(selectField_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  border-bottom: None;\n  padding-right: 16px;\n"], ["\n  border-bottom: None;\n  padding-right: 16px;\n"])));
var FileResult = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  width: inherit;\n"], ["\n  width: inherit;\n"])));
var NoSourceFileBody = styled_1.default(panels_1.PanelBody)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  padding: 12px;\n  grid-template-columns: 30px 1fr;\n  align-items: center;\n"], ["\n  display: grid;\n  padding: 12px;\n  grid-template-columns: 30px 1fr;\n  align-items: center;\n"])));
var SourceFileBody = styled_1.default(panels_1.PanelBody)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  padding: 12px;\n  grid-template-columns: 30px 1fr 100px;\n  align-items: center;\n"], ["\n  display: grid;\n  padding: 12px;\n  grid-template-columns: 30px 1fr 100px;\n  align-items: center;\n"])));
var IntegrationsList = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  justify-items: center;\n  margin-top: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  justify-items: center;\n  margin-top: ", ";\n"])), space_1.default(1), space_1.default(2));
var IntegrationName = styled_1.default('p')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  padding-left: 10px;\n"], ["\n  padding-left: 10px;\n"])));
var Container = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n"], ["\n  display: flex;\n  justify-content: center;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=addCodeOwnerModal.jsx.map