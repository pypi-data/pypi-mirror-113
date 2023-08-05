Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var styles_1 = require("app/components/charts/styles");
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var groupList_1 = tslib_1.__importDefault(require("app/components/issues/groupList"));
var panels_1 = require("app/components/panels");
var constants_1 = require("app/constants");
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var fields_1 = require("app/utils/discover/fields");
var queryString_1 = require("app/utils/queryString");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var EXCLUDE_TAG_KEYS = new Set([
    // event type can be "transaction" but we're searching for issues
    'event.type',
    // the project is already determined by the transaction,
    // and issue search does not support the project filter
    'project',
]);
var RelatedIssues = /** @class */ (function (_super) {
    tslib_1.__extends(RelatedIssues, _super);
    function RelatedIssues() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleOpenClick = function () {
            var organization = _this.props.organization;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'performance_views.summary.open_issues',
                eventName: 'Performance Views: Open issues from transaction summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
        _this.renderEmptyMessage = function () {
            var statsPeriod = _this.props.statsPeriod;
            var selectedTimePeriod = statsPeriod && constants_1.DEFAULT_RELATIVE_PERIODS[statsPeriod];
            var displayedPeriod = selectedTimePeriod
                ? selectedTimePeriod.toLowerCase()
                : locale_1.t('given timeframe');
            return (<panels_1.Panel>
        <panels_1.PanelBody>
          <emptyStateWarning_1.default>
            <p>
              {locale_1.tct('No new issues for this transaction for the [timePeriod].', {
                    timePeriod: displayedPeriod,
                })}
            </p>
          </emptyStateWarning_1.default>
        </panels_1.PanelBody>
      </panels_1.Panel>);
        };
        return _this;
    }
    RelatedIssues.prototype.getIssuesEndpoint = function () {
        var _a = this.props, transaction = _a.transaction, organization = _a.organization, start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod, location = _a.location;
        var queryParams = tslib_1.__assign({ start: start, end: end, statsPeriod: statsPeriod, limit: 5, sort: 'new' }, pick_1.default(location.query, tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(Object.values(globalSelectionHeader_1.URL_PARAM))), ['cursor'])));
        var currentFilter = tokenizeSearch_1.tokenizeSearch(queryString_1.decodeScalar(location.query.query, ''));
        currentFilter.getTagKeys().forEach(function (tagKey) {
            var searchKey = tagKey.startsWith('!') ? tagKey.substr(1) : tagKey;
            // Remove aggregates and transaction event fields
            if (
            // aggregates
            searchKey.match(/\w+\(.*\)/) ||
                // transaction event fields
                fields_1.TRACING_FIELDS.includes(searchKey) ||
                // tags that we dont want to pass to pass to issue search
                EXCLUDE_TAG_KEYS.has(searchKey)) {
                currentFilter.removeTag(tagKey);
            }
        });
        currentFilter.addQuery('is:unresolved').setTagValues('transaction', [transaction]);
        return {
            path: "/organizations/" + organization.slug + "/issues/",
            queryParams: tslib_1.__assign(tslib_1.__assign({}, queryParams), { query: currentFilter.formatString() }),
        };
    };
    RelatedIssues.prototype.render = function () {
        var organization = this.props.organization;
        var _a = this.getIssuesEndpoint(), path = _a.path, queryParams = _a.queryParams;
        var issueSearch = {
            pathname: "/organizations/" + organization.slug + "/issues/",
            query: queryParams,
        };
        return (<react_1.Fragment>
        <ControlsWrapper>
          <styles_1.SectionHeading>{locale_1.t('Related Issues')}</styles_1.SectionHeading>
          <button_1.default data-test-id="issues-open" size="small" to={issueSearch} onClick={this.handleOpenClick}>
            {locale_1.t('Open in Issues')}
          </button_1.default>
        </ControlsWrapper>

        <TableWrapper>
          <groupList_1.default orgId={organization.slug} endpointPath={path} queryParams={queryParams} query="" canSelectGroups={false} renderEmptyMessage={this.renderEmptyMessage} withChart={false} withPagination={false}/>
        </TableWrapper>
      </react_1.Fragment>);
    };
    return RelatedIssues;
}(react_1.Component));
var ControlsWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), space_1.default(1));
var TableWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"], ["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"])), space_1.default(4), panels_1.Panel, space_1.default(1));
exports.default = RelatedIssues;
var templateObject_1, templateObject_2;
//# sourceMappingURL=relatedIssues.jsx.map