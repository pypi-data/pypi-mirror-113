Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var panels_1 = require("app/components/panels");
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("./utils");
function SessionRow(_a) {
    var ipAddress = _a.ipAddress, lastSeen = _a.lastSeen, firstSeen = _a.firstSeen, countryCode = _a.countryCode, regionCode = _a.regionCode;
    return (<SessionPanelItem>
      <IpAndLocation>
        <IpAddress>{ipAddress}</IpAddress>
        {countryCode && regionCode && (<CountryCode>{countryCode + " (" + regionCode + ")"}</CountryCode>)}
      </IpAndLocation>
      <StyledTimeSince date={firstSeen}/>
      <StyledTimeSince date={lastSeen}/>
    </SessionPanelItem>);
}
exports.default = SessionRow;
var IpAddress = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  font-weight: bold;\n"], ["\n  margin-bottom: ", ";\n  font-weight: bold;\n"])), space_1.default(0.5));
var CountryCode = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeRelativeSmall; });
var StyledTimeSince = styled_1.default(timeSince_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeRelativeSmall; });
var IpAndLocation = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var SessionPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), utils_1.tableLayout);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=sessionRow.jsx.map