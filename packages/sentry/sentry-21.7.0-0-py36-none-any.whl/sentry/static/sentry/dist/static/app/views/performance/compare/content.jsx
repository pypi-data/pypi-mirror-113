Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var breadcrumb_1 = tslib_1.__importDefault(require("app/views/performance/breadcrumb"));
var traceView_1 = tslib_1.__importDefault(require("./traceView"));
var transactionSummary_1 = tslib_1.__importDefault(require("./transactionSummary"));
var utils_1 = require("./utils");
var TransactionComparisonContent = /** @class */ (function (_super) {
    tslib_1.__extends(TransactionComparisonContent, _super);
    function TransactionComparisonContent() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TransactionComparisonContent.prototype.getTransactionName = function () {
        var _a = this.props, baselineEvent = _a.baselineEvent, regressionEvent = _a.regressionEvent;
        if (utils_1.isTransactionEvent(baselineEvent) && utils_1.isTransactionEvent(regressionEvent)) {
            if (baselineEvent.title === regressionEvent.title) {
                return baselineEvent.title;
            }
            return locale_1.t('mixed transaction names');
        }
        if (utils_1.isTransactionEvent(baselineEvent)) {
            return baselineEvent.title;
        }
        if (utils_1.isTransactionEvent(regressionEvent)) {
            return regressionEvent.title;
        }
        return locale_1.t('no transaction title found');
    };
    TransactionComparisonContent.prototype.render = function () {
        var _a = this.props, baselineEvent = _a.baselineEvent, regressionEvent = _a.regressionEvent, organization = _a.organization, location = _a.location, params = _a.params;
        var transactionName = baselineEvent.title === regressionEvent.title ? baselineEvent.title : undefined;
        return (<react_1.Fragment>
        <Layout.Header>
          <Layout.HeaderContent>
            <breadcrumb_1.default organization={organization} location={location} transactionName={transactionName} transactionComparison/>
            <Layout.Title>{this.getTransactionName()}</Layout.Title>
          </Layout.HeaderContent>
          <Layout.HeaderActions>
            <transactionSummary_1.default organization={organization} location={location} params={params} baselineEvent={baselineEvent} regressionEvent={regressionEvent}/>
          </Layout.HeaderActions>
        </Layout.Header>
        <Layout.Body>
          <StyledPanel>
            <traceView_1.default baselineEvent={baselineEvent} regressionEvent={regressionEvent}/>
          </StyledPanel>
        </Layout.Body>
      </react_1.Fragment>);
    };
    return TransactionComparisonContent;
}(react_1.Component));
var StyledPanel = styled_1.default(panels_1.Panel)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  grid-column: 1 / span 2;\n  overflow: hidden;\n"], ["\n  grid-column: 1 / span 2;\n  overflow: hidden;\n"])));
exports.default = TransactionComparisonContent;
var templateObject_1;
//# sourceMappingURL=content.jsx.map