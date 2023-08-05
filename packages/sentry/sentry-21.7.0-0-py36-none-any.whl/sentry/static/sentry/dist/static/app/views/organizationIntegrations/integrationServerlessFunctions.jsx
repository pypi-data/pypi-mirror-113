Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
// eslint-disable-next-line simple-import-sort/imports
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var panels_1 = require("app/components/panels");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var locale_1 = require("app/locale");
var integrationUtil_1 = require("app/utils/integrationUtil");
var integrationServerlessRow_1 = tslib_1.__importDefault(require("./integrationServerlessRow"));
var IntegrationServerlessFunctions = /** @class */ (function (_super) {
    tslib_1.__extends(IntegrationServerlessFunctions, _super);
    function IntegrationServerlessFunctions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleFunctionUpdate = function (serverlessFunctionUpdate, index) {
            var serverlessFunctions = tslib_1.__spreadArray([], tslib_1.__read(_this.serverlessFunctions));
            var serverlessFunction = tslib_1.__assign(tslib_1.__assign({}, serverlessFunctions[index]), serverlessFunctionUpdate);
            serverlessFunctions[index] = serverlessFunction;
            _this.setState({ serverlessFunctions: serverlessFunctions });
        };
        return _this;
    }
    IntegrationServerlessFunctions.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { serverlessFunctions: [] });
    };
    IntegrationServerlessFunctions.prototype.getEndpoints = function () {
        var orgSlug = this.props.organization.slug;
        return [
            [
                'serverlessFunctions',
                "/organizations/" + orgSlug + "/integrations/" + this.props.integration.id + "/serverless-functions/",
            ],
        ];
    };
    Object.defineProperty(IntegrationServerlessFunctions.prototype, "serverlessFunctions", {
        get: function () {
            return this.state.serverlessFunctions;
        },
        enumerable: false,
        configurable: true
    });
    IntegrationServerlessFunctions.prototype.onLoadAllEndpointsSuccess = function () {
        integrationUtil_1.trackIntegrationEvent('integrations.serverless_functions_viewed', {
            integration: this.props.integration.provider.key,
            integration_type: 'first_party',
            num_functions: this.serverlessFunctions.length,
        }, this.props.organization);
    };
    IntegrationServerlessFunctions.prototype.renderBody = function () {
        var _this = this;
        return (<react_1.Fragment>
        <alert_1.default type="info">
          {locale_1.t('Manage your AWS Lambda functions below. Only Node and Python runtimes are currently supported.')}
        </alert_1.default>
        <panels_1.Panel>
          <StyledPanelHeader disablePadding hasButtons>
            <NameHeader>{locale_1.t('Name')}</NameHeader>
            <LayerStatusWrapper>{locale_1.t('Layer Status')}</LayerStatusWrapper>
            <EnableHeader>{locale_1.t('Enabled')}</EnableHeader>
          </StyledPanelHeader>
          <StyledPanelBody>
            {this.serverlessFunctions.map(function (serverlessFunction, i) { return (<integrationServerlessRow_1.default key={serverlessFunction.name} serverlessFunction={serverlessFunction} onUpdateFunction={function (update) {
                    return _this.handleFunctionUpdate(update, i);
                }} {..._this.props}/>); })}
          </StyledPanelBody>
        </panels_1.Panel>
      </react_1.Fragment>);
    };
    return IntegrationServerlessFunctions;
}(asyncComponent_1.default));
exports.default = withOrganization_1.default(IntegrationServerlessFunctions);
var StyledPanelHeader = styled_1.default(panels_1.PanelHeader)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  display: grid;\n  grid-column-gap: ", ";\n  align-items: center;\n  grid-template-columns: 2fr 1fr 0.5fr;\n  grid-template-areas: 'function-name layer-status enable-switch';\n"], ["\n  padding: ", ";\n  display: grid;\n  grid-column-gap: ", ";\n  align-items: center;\n  grid-template-columns: 2fr 1fr 0.5fr;\n  grid-template-areas: 'function-name layer-status enable-switch';\n"])), space_1.default(2), space_1.default(1));
var HeaderText = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var StyledPanelBody = styled_1.default(panels_1.PanelBody)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject([""], [""])));
var NameHeader = styled_1.default(HeaderText)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  grid-area: function-name;\n"], ["\n  grid-area: function-name;\n"])));
var LayerStatusWrapper = styled_1.default(HeaderText)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  grid-area: layer-status;\n"], ["\n  grid-area: layer-status;\n"])));
var EnableHeader = styled_1.default(HeaderText)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  grid-area: enable-switch;\n"], ["\n  grid-area: enable-switch;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=integrationServerlessFunctions.jsx.map