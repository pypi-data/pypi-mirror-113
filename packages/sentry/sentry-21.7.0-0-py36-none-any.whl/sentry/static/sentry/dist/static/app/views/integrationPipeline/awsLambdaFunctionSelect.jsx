Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var reduce_1 = tslib_1.__importDefault(require("lodash/reduce"));
var mobx_1 = require("mobx");
var mobx_react_1 = require("mobx-react");
var list_1 = tslib_1.__importDefault(require("app/components/list"));
var listItem_1 = tslib_1.__importDefault(require("app/components/list/listItem"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panels_1 = require("app/components/panels");
var switchButton_1 = tslib_1.__importDefault(require("app/components/switchButton"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var model_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/model"));
var footerWithButtons_1 = tslib_1.__importDefault(require("./components/footerWithButtons"));
var headerWithHelp_1 = tslib_1.__importDefault(require("./components/headerWithHelp"));
var LAMBDA_COUNT_THRESHOLD = 10;
var getLabel = function (func) { return func.FunctionName; };
var AwsLambdaFunctionSelect = /** @class */ (function (_super) {
    tslib_1.__extends(AwsLambdaFunctionSelect, _super);
    function AwsLambdaFunctionSelect(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            submitting: false,
        };
        _this.model = new model_1.default({ apiOptions: { baseUrl: window.location.origin } });
        _this.handleSubmit = function () {
            _this.model.saveForm();
            _this.setState({ submitting: true });
        };
        _this.handleToggle = function () {
            var newState = !_this.allStatesToggled;
            _this.lambdaFunctions.forEach(function (lambda) {
                _this.model.setValue(lambda.FunctionName, newState, { quiet: true });
            });
        };
        _this.renderWhatWeFound = function () {
            var count = _this.lambdaFunctions.length;
            return (<h4>
        {locale_1.tn('We found %s function with a Node or Python runtime', 'We found %s functions with Node or Python runtimes', count)}
      </h4>);
        };
        _this.renderLoadingScreen = function () {
            var count = _this.enabledCount;
            var text = count > LAMBDA_COUNT_THRESHOLD
                ? locale_1.t('This might take a while\u2026', count)
                : locale_1.t('This might take a sec\u2026');
            return (<LoadingWrapper>
        <StyledLoadingIndicator />
        <h4>{locale_1.t('Adding Sentry to %s functions', count)}</h4>
        {text}
      </LoadingWrapper>);
        };
        _this.renderCore = function () {
            var initialStepNumber = _this.props.initialStepNumber;
            var FormHeader = (<StyledPanelHeader>
        {locale_1.t('Lambda Functions')}
        <SwitchHolder>
          <mobx_react_1.Observer>
            {function () { return (<tooltip_1.default title={_this.allStatesToggled ? locale_1.t('Disable All') : locale_1.t('Enable All')} position="left">
                <StyledSwitch size="lg" name="toggleAll" toggle={_this.handleToggle} isActive={_this.allStatesToggled}/>
              </tooltip_1.default>); }}
          </mobx_react_1.Observer>
        </SwitchHolder>
      </StyledPanelHeader>);
            var formFields = {
                fields: _this.lambdaFunctions.map(function (func) { return ({
                    name: func.FunctionName,
                    type: 'boolean',
                    required: false,
                    label: getLabel(func),
                    alignRight: true,
                }); }),
            };
            return (<list_1.default symbol="colored-numeric" initialCounterValue={initialStepNumber}>
        <listItem_1.default>
          <Header>{_this.renderWhatWeFound()}</Header>
          {locale_1.t('Decide which functions you would like to enable for Sentry monitoring')}
          <StyledForm initialData={_this.initialData} skipPreventDefault model={_this.model} apiEndpoint="/extensions/aws_lambda/setup/" hideFooter>
            <jsonForm_1.default renderHeader={function () { return FormHeader; }} forms={[formFields]}/>
          </StyledForm>
        </listItem_1.default>
        <react_1.Fragment />
      </list_1.default>);
        };
        mobx_1.makeObservable(_this, { allStatesToggled: mobx_1.computed });
        return _this;
    }
    Object.defineProperty(AwsLambdaFunctionSelect.prototype, "initialData", {
        get: function () {
            var lambdaFunctions = this.props.lambdaFunctions;
            var initialData = lambdaFunctions.reduce(function (accum, func) {
                accum[func.FunctionName] = true;
                return accum;
            }, {});
            return initialData;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AwsLambdaFunctionSelect.prototype, "lambdaFunctions", {
        get: function () {
            return this.props.lambdaFunctions.sort(function (a, b) {
                return getLabel(a).toLowerCase() < getLabel(b).toLowerCase() ? -1 : 1;
            });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AwsLambdaFunctionSelect.prototype, "enabledCount", {
        get: function () {
            var data = this.model.getTransformedData();
            return reduce_1.default(data, function (acc, val) { return (val ? acc + 1 : acc); }, 0);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AwsLambdaFunctionSelect.prototype, "allStatesToggled", {
        get: function () {
            // check if any of the lambda functions have a falsy value
            // no falsy values means everything is enabled
            return Object.values(this.model.getData()).every(function (val) { return val; });
        },
        enumerable: false,
        configurable: true
    });
    AwsLambdaFunctionSelect.prototype.render = function () {
        var _this = this;
        return (<react_1.Fragment>
        <headerWithHelp_1.default docsUrl="https://docs.sentry.io/product/integrations/aws-lambda/"/>
        <Wrapper>
          {this.state.submitting ? this.renderLoadingScreen() : this.renderCore()}
        </Wrapper>
        <mobx_react_1.Observer>
          {function () { return (<footerWithButtons_1.default buttonText={locale_1.t('Finish Setup')} onClick={_this.handleSubmit} disabled={_this.model.isError || _this.model.isSaving}/>); }}
        </mobx_react_1.Observer>
      </react_1.Fragment>);
    };
    return AwsLambdaFunctionSelect;
}(react_1.Component));
exports.default = AwsLambdaFunctionSelect;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 100px 50px 50px 50px;\n"], ["\n  padding: 100px 50px 50px 50px;\n"])));
// TODO(ts): Understand why styled is not correctly inheriting props here
var StyledForm = styled_1.default(form_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-top: 10px;\n"], ["\n  margin-top: 10px;\n"])));
var Header = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  text-align: left;\n  margin-bottom: 10px;\n"], ["\n  text-align: left;\n  margin-bottom: 10px;\n"])));
var LoadingWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  padding: 50px;\n  text-align: center;\n"], ["\n  padding: 50px;\n  text-align: center;\n"])));
var StyledLoadingIndicator = styled_1.default(loadingIndicator_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var SwitchHolder = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var StyledSwitch = styled_1.default(switchButton_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin: auto;\n"], ["\n  margin: auto;\n"])));
// padding is based on fom control width
var StyledPanelHeader = styled_1.default(panels_1.PanelHeader)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  padding-right: 36px;\n"], ["\n  padding-right: 36px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=awsLambdaFunctionSelect.jsx.map