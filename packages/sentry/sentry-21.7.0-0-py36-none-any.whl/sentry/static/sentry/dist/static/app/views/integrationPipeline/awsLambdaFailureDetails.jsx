Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var footerWithButtons_1 = tslib_1.__importDefault(require("./components/footerWithButtons"));
var headerWithHelp_1 = tslib_1.__importDefault(require("./components/headerWithHelp"));
function AwsLambdaFailureDetails(_a) {
    var lambdaFunctionFailures = _a.lambdaFunctionFailures, successCount = _a.successCount;
    var baseDocsUrl = 'https://docs.sentry.io/product/integrations/aws-lambda/';
    return (<react_1.Fragment>
      <headerWithHelp_1.default docsUrl={baseDocsUrl}/>
      <Wrapper>
        <div>
          <StyledCheckmark isCircled color="green300"/>
          <h3>
            {locale_1.tn('successfully updated %s function', 'successfully updated %s functions', successCount)}
          </h3>
        </div>
        <div>
          <StyledWarning color="red300"/>
          <h3>
            {locale_1.tn('Failed to update %s function', 'Failed to update %s functions', lambdaFunctionFailures.length)}
          </h3>
          <Troubleshooting>
            {locale_1.tct('See [link:Troubleshooting Docs]', {
            link: <externalLink_1.default href={baseDocsUrl + '#troubleshooting'}/>,
        })}
          </Troubleshooting>
        </div>
        <StyledPanel>{lambdaFunctionFailures.map(SingleFailure)}</StyledPanel>
      </Wrapper>
      <footerWithButtons_1.default buttonText={locale_1.t('Finish Setup')} href="?finish_pipeline=1"/>
    </react_1.Fragment>);
}
exports.default = AwsLambdaFailureDetails;
function SingleFailure(errorDetail) {
    return (<StyledRow key={errorDetail.name}>
      <span>{errorDetail.name}</span>
      <Error>{errorDetail.error}</Error>
    </StyledRow>);
}
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 100px 50px 50px 50px;\n"], ["\n  padding: 100px 50px 50px 50px;\n"])));
var StyledRow = styled_1.default(panels_1.PanelItem)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
var Error = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var StyledPanel = styled_1.default(panels_1.Panel)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  margin-left: 34px;\n"], ["\n  overflow: hidden;\n  margin-left: 34px;\n"])));
var Troubleshooting = styled_1.default('p')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin-left: 34px;\n"], ["\n  margin-left: 34px;\n"])));
var StyledCheckmark = styled_1.default(icons_1.IconCheckmark)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  float: left;\n  margin-right: 10px;\n  height: 24px;\n  width: 24px;\n"], ["\n  float: left;\n  margin-right: 10px;\n  height: 24px;\n  width: 24px;\n"])));
var StyledWarning = styled_1.default(icons_1.IconWarning)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  float: left;\n  margin-right: 10px;\n  height: 24px;\n  width: 24px;\n"], ["\n  float: left;\n  margin-right: 10px;\n  height: 24px;\n  width: 24px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=awsLambdaFailureDetails.jsx.map