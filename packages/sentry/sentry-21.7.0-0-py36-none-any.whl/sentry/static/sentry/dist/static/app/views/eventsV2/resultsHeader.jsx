Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var discoverSavedQueries_1 = require("app/actionCreators/discoverSavedQueries");
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var breadcrumb_1 = tslib_1.__importDefault(require("./breadcrumb"));
var eventInputName_1 = tslib_1.__importDefault(require("./eventInputName"));
var savedQuery_1 = tslib_1.__importDefault(require("./savedQuery"));
var ResultsHeader = /** @class */ (function (_super) {
    tslib_1.__extends(ResultsHeader, _super);
    function ResultsHeader() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            savedQuery: undefined,
            loading: true,
        };
        return _this;
    }
    ResultsHeader.prototype.componentDidMount = function () {
        if (this.props.eventView.id) {
            this.fetchData();
        }
    };
    ResultsHeader.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.eventView &&
            this.props.eventView &&
            prevProps.eventView.id !== this.props.eventView.id) {
            this.fetchData();
        }
    };
    ResultsHeader.prototype.fetchData = function () {
        var _this = this;
        var _a = this.props, api = _a.api, eventView = _a.eventView, organization = _a.organization;
        if (typeof eventView.id === 'string') {
            this.setState({ loading: true });
            discoverSavedQueries_1.fetchSavedQuery(api, organization.slug, eventView.id).then(function (savedQuery) {
                _this.setState({ savedQuery: savedQuery, loading: false });
            });
        }
    };
    ResultsHeader.prototype.renderAuthor = function () {
        var _a;
        var eventView = this.props.eventView;
        var savedQuery = this.state.savedQuery;
        // No saved query in use.
        if (!eventView.id) {
            return null;
        }
        var createdBy = ' \u2014 ';
        var lastEdit = ' \u2014 ';
        if (savedQuery !== undefined) {
            createdBy = ((_a = savedQuery.createdBy) === null || _a === void 0 ? void 0 : _a.email) || '\u2014';
            lastEdit = <timeSince_1.default date={savedQuery.dateUpdated}/>;
        }
        return (<Subtitle>
        {locale_1.t('Created by:')} {createdBy} | {locale_1.t('Last edited:')} {lastEdit}
      </Subtitle>);
    };
    ResultsHeader.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, location = _a.location, errorCode = _a.errorCode, eventView = _a.eventView, onIncompatibleAlertQuery = _a.onIncompatibleAlertQuery;
        var _b = this.state, savedQuery = _b.savedQuery, loading = _b.loading;
        return (<Layout.Header>
        <StyledHeaderContent>
          <breadcrumb_1.default eventView={eventView} organization={organization} location={location}/>
          <eventInputName_1.default savedQuery={savedQuery} organization={organization} eventView={eventView}/>
          {this.renderAuthor()}
        </StyledHeaderContent>
        <Layout.HeaderActions>
          <savedQuery_1.default location={location} organization={organization} eventView={eventView} savedQuery={savedQuery} savedQueryLoading={loading} disabled={errorCode >= 400 && errorCode < 500} updateCallback={function () { return _this.fetchData(); }} onIncompatibleAlertQuery={onIncompatibleAlertQuery}/>
        </Layout.HeaderActions>
      </Layout.Header>);
    };
    return ResultsHeader;
}(React.Component));
var Subtitle = styled_1.default('h4')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  font-weight: normal;\n  color: ", ";\n  margin: ", " 0 0 0;\n"], ["\n  font-size: ", ";\n  font-weight: normal;\n  color: ", ";\n  margin: ", " 0 0 0;\n"])), function (p) { return p.theme.fontSizeLarge; }, function (p) { return p.theme.gray300; }, space_1.default(0.5));
var StyledHeaderContent = styled_1.default(Layout.HeaderContent)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  overflow: unset;\n"], ["\n  overflow: unset;\n"])));
exports.default = withApi_1.default(ResultsHeader);
var templateObject_1, templateObject_2;
//# sourceMappingURL=resultsHeader.jsx.map