Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importDefault(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var lightWeightNoProjectMessage_1 = tslib_1.__importDefault(require("app/components/lightWeightNoProjectMessage"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var data_1 = require("../data");
var content_1 = tslib_1.__importDefault(require("./content"));
var TrendsSummary = /** @class */ (function (_super) {
    tslib_1.__extends(TrendsSummary, _super);
    function TrendsSummary() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: data_1.generatePerformanceEventView(_this.props.organization, _this.props.location, _this.props.projects, true),
            error: undefined,
        };
        _this.setError = function (error) {
            _this.setState({ error: error });
        };
        return _this;
    }
    TrendsSummary.getDerivedStateFromProps = function (nextProps, prevState) {
        return tslib_1.__assign(tslib_1.__assign({}, prevState), { eventView: data_1.generatePerformanceEventView(nextProps.organization, nextProps.location, nextProps.projects, true) });
    };
    TrendsSummary.prototype.getDocumentTitle = function () {
        return [locale_1.t('Trends'), locale_1.t('Performance')].join(' - ');
    };
    TrendsSummary.prototype.renderContent = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        var eventView = this.state.eventView;
        return (<content_1.default organization={organization} location={location} eventView={eventView}/>);
    };
    TrendsSummary.prototype.render = function () {
        var organization = this.props.organization;
        return (<sentryDocumentTitle_1.default title={this.getDocumentTitle()} orgSlug={organization.slug}>
        <StyledPageContent>
          <lightWeightNoProjectMessage_1.default organization={organization}>
            {this.renderContent()}
          </lightWeightNoProjectMessage_1.default>
        </StyledPageContent>
      </sentryDocumentTitle_1.default>);
    };
    return TrendsSummary;
}(react_1.default.Component));
exports.default = withOrganization_1.default(withProjects_1.default(withGlobalSelection_1.default(withApi_1.default(TrendsSummary))));
var StyledPageContent = styled_1.default(organization_1.PageContent)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map