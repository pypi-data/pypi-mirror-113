Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var mobx_react_1 = require("mobx-react");
var qs = tslib_1.__importStar(require("query-string"));
var indicator_1 = require("app/actionCreators/indicator");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var list_1 = tslib_1.__importDefault(require("app/components/list"));
var listItem_1 = tslib_1.__importDefault(require("app/components/list/listItem"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var model_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/model"));
var sentryProjectSelectorField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/sentryProjectSelectorField"));
var footerWithButtons_1 = tslib_1.__importDefault(require("./components/footerWithButtons"));
var headerWithHelp_1 = tslib_1.__importDefault(require("./components/headerWithHelp"));
var AwsLambdaProjectSelect = /** @class */ (function (_super) {
    tslib_1.__extends(AwsLambdaProjectSelect, _super);
    function AwsLambdaProjectSelect() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.model = new model_1.default();
        _this.handleSubmit = function (e) {
            e.preventDefault();
            var data = _this.model.getData();
            indicator_1.addLoadingMessage(locale_1.t('Submitting\u2026'));
            _this.model.setFormSaving();
            var origin = window.location.origin;
            // redirect to the extensions endpoint with the form fields as query params
            // this is needed so we don't restart the pipeline loading from the original
            // OrganizationIntegrationSetupView route
            var newUrl = origin + "/extensions/aws_lambda/setup/?" + qs.stringify(data);
            window.location.assign(newUrl);
        };
        return _this;
    }
    AwsLambdaProjectSelect.prototype.render = function () {
        var _this = this;
        var projects = this.props.projects;
        // TODO: Add logic if no projects
        return (<React.Fragment>
        <headerWithHelp_1.default docsUrl="https://docs.sentry.io/product/integrations/aws-lambda/"/>
        <StyledList symbol="colored-numeric">
          <React.Fragment />
          <listItem_1.default>
            <h3>{locale_1.t('Select a project for your AWS Lambdas')}</h3>
            <form_1.default model={this.model} hideFooter>
              <StyledSentryProjectSelectorField placeholder={locale_1.t('Select a project')} name="projectId" projects={projects} inline={false} hasControlState flexibleControlStateSize stacked/>
              <alert_1.default type="info">
                {locale_1.t('Currently only supports Node and Python Lambda functions')}
              </alert_1.default>
            </form_1.default>
          </listItem_1.default>
        </StyledList>
        <mobx_react_1.Observer>
          {function () { return (<footerWithButtons_1.default buttonText={locale_1.t('Next')} onClick={_this.handleSubmit} disabled={_this.model.isSaving || !_this.model.getValue('projectId')}/>); }}
        </mobx_react_1.Observer>
      </React.Fragment>);
    };
    return AwsLambdaProjectSelect;
}(React.Component));
exports.default = AwsLambdaProjectSelect;
var StyledList = styled_1.default(list_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 100px 50px 50px 50px;\n"], ["\n  padding: 100px 50px 50px 50px;\n"])));
var StyledSentryProjectSelectorField = styled_1.default(sentryProjectSelectorField_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: 0 0 ", " 0;\n"], ["\n  padding: 0 0 ", " 0;\n"])), space_1.default(2));
var templateObject_1, templateObject_2;
//# sourceMappingURL=awsLambdaProjectSelect.jsx.map