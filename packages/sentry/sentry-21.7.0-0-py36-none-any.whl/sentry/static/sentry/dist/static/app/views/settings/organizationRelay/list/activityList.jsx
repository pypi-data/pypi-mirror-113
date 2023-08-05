Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var ActivityList = function (_a) {
    var activities = _a.activities;
    return (<StyledPanelTable headers={[locale_1.t('Version'), locale_1.t('First Used'), locale_1.t('Last Used')]}>
    {activities.map(function (_a) {
            var relayId = _a.relayId, version = _a.version, firstSeen = _a.firstSeen, lastSeen = _a.lastSeen;
            return (<react_1.Fragment key={relayId}>
          <div>{version}</div>
          <dateTime_1.default date={firstSeen} seconds={false}/>
          <dateTime_1.default date={lastSeen} seconds={false}/>
        </react_1.Fragment>);
        })}
  </StyledPanelTable>);
};
exports.default = ActivityList;
var StyledPanelTable = styled_1.default(panels_1.PanelTable)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: repeat(3, 2fr);\n\n  @media (min-width: ", ") {\n    grid-template-columns: 2fr repeat(2, 1fr);\n  }\n"], ["\n  grid-template-columns: repeat(3, 2fr);\n\n  @media (min-width: ", ") {\n    grid-template-columns: 2fr repeat(2, 1fr);\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var templateObject_1;
//# sourceMappingURL=activityList.jsx.map