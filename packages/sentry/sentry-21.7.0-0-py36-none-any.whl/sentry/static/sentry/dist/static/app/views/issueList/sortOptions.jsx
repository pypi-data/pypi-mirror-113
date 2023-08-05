Object.defineProperty(exports, "__esModule", { value: true });
exports.getSortTooltip = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var dropdownControl_1 = tslib_1.__importStar(require("app/components/dropdownControl"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var utils_1 = require("app/views/issueList/utils");
function getSortTooltip(key) {
    switch (key) {
        case utils_1.IssueSortOptions.INBOX:
            return locale_1.t('When the issue was flagged for review.');
        case utils_1.IssueSortOptions.NEW:
            return locale_1.t('When the issue was first seen in the selected time period.');
        case utils_1.IssueSortOptions.PRIORITY:
            return locale_1.t('Issues trending upward recently.');
        case utils_1.IssueSortOptions.FREQ:
            return locale_1.t('Number of events in the time selected.');
        case utils_1.IssueSortOptions.USER:
            return locale_1.t('Number of users affected in the time selected.');
        case utils_1.IssueSortOptions.TREND:
            return locale_1.t('% change in event count over the time selected.');
        case utils_1.IssueSortOptions.DATE:
        default:
            return locale_1.t('When the issue was last seen in the selected time period.');
    }
}
exports.getSortTooltip = getSortTooltip;
var IssueListSortOptions = function (_a) {
    var onSelect = _a.onSelect, sort = _a.sort, query = _a.query;
    var sortKey = sort || utils_1.IssueSortOptions.DATE;
    var getMenuItem = function (key) { return (<dropdownControl_1.DropdownItem onSelect={onSelect} eventKey={key} isActive={sortKey === key}>
      <StyledTooltip containerDisplayMode="block" position="top" delay={500} title={getSortTooltip(key)}>
        {utils_1.getSortLabel(key)}
      </StyledTooltip>
    </dropdownControl_1.DropdownItem>); };
    return (<dropdownControl_1.default buttonProps={{ prefix: locale_1.t('Sort by') }} label={utils_1.getSortLabel(sortKey)}>
      <React.Fragment>
        {query === utils_1.Query.FOR_REVIEW && getMenuItem(utils_1.IssueSortOptions.INBOX)}
        {getMenuItem(utils_1.IssueSortOptions.DATE)}
        {getMenuItem(utils_1.IssueSortOptions.NEW)}
        {getMenuItem(utils_1.IssueSortOptions.PRIORITY)}
        {getMenuItem(utils_1.IssueSortOptions.FREQ)}
        {getMenuItem(utils_1.IssueSortOptions.USER)}
        <feature_1.default features={['issue-list-trend-sort']}>
          {getMenuItem(utils_1.IssueSortOptions.TREND)}
        </feature_1.default>
      </React.Fragment>
    </dropdownControl_1.default>);
};
exports.default = IssueListSortOptions;
var StyledTooltip = styled_1.default(tooltip_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n"], ["\n  width: 100%;\n"])));
var templateObject_1;
//# sourceMappingURL=sortOptions.jsx.map