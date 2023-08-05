Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
// This is required to offer components that sit between this settings header
// and i.e. dropdowns, some zIndex layer room
//
// e.g. app/views/settings/incidentRules/triggers/chart/
var HEADER_Z_INDEX_OFFSET = 5;
var SettingsHeader = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: sticky;\n  top: 0;\n  z-index: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  height: ", ";\n"], ["\n  position: sticky;\n  top: 0;\n  z-index: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  height: ", ";\n"])), function (p) { return p.theme.zIndex.header + HEADER_Z_INDEX_OFFSET; }, space_1.default(3), space_1.default(4), function (p) { return p.theme.border; }, function (p) { return p.theme.background; }, function (p) { return p.theme.settings.headerHeight; });
exports.default = SettingsHeader;
var templateObject_1;
//# sourceMappingURL=settingsHeader.jsx.map