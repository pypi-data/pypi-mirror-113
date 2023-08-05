Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importDefault(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var dropdownControl_1 = tslib_1.__importStar(require("app/components/dropdownControl"));
var featureBadge_1 = tslib_1.__importDefault(require("app/components/featureBadge"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var utils_1 = require("app/views/issueList/utils");
var IssueListDisplayOptions = function (_a) {
    var onDisplayChange = _a.onDisplayChange, display = _a.display, hasSessions = _a.hasSessions, hasMultipleProjectsSelected = _a.hasMultipleProjectsSelected;
    var getMenuItem = function (key) {
        var tooltipText;
        var disabled = false;
        if (key === utils_1.IssueDisplayOptions.SESSIONS) {
            if (hasMultipleProjectsSelected) {
                tooltipText = locale_1.t('This option is not available when multiple projects are selected.');
                disabled = true;
            }
            else if (!hasSessions) {
                tooltipText = locale_1.t('This option is not available because there is no session data in the selected time period.');
                disabled = true;
            }
        }
        return (<dropdownControl_1.DropdownItem onSelect={onDisplayChange} eventKey={key} isActive={key === display} disabled={disabled}>
        <StyledTooltip containerDisplayMode="block" position="top" title={tooltipText} disabled={!tooltipText}>
          {utils_1.getDisplayLabel(key)}
          {key === utils_1.IssueDisplayOptions.SESSIONS && <featureBadge_1.default type="beta" noTooltip/>}
        </StyledTooltip>
      </dropdownControl_1.DropdownItem>);
    };
    return (<guideAnchor_1.default target="percentage_based_alerts" position="bottom" disabled={!hasSessions || hasMultipleProjectsSelected}>
      <dropdownControl_1.default buttonProps={{ prefix: locale_1.t('Display') }} buttonTooltipTitle={display === utils_1.IssueDisplayOptions.SESSIONS
            ? locale_1.t('This shows the event count as a percent of sessions in the same time period.')
            : null} label={!hasSessions || hasMultipleProjectsSelected
            ? utils_1.getDisplayLabel(utils_1.IssueDisplayOptions.EVENTS)
            : utils_1.getDisplayLabel(display)}>
        <react_1.default.Fragment>
          {getMenuItem(utils_1.IssueDisplayOptions.EVENTS)}
          {getMenuItem(utils_1.IssueDisplayOptions.SESSIONS)}
        </react_1.default.Fragment>
      </dropdownControl_1.default>
    </guideAnchor_1.default>);
};
var StyledTooltip = styled_1.default(tooltip_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n"], ["\n  width: 100%;\n"])));
exports.default = IssueListDisplayOptions;
var templateObject_1;
//# sourceMappingURL=displayOptions.jsx.map