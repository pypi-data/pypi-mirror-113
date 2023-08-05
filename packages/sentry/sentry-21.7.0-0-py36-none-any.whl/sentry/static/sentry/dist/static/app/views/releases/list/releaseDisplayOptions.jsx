var _a;
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var locale_1 = require("app/locale");
var releaseListDropdown_1 = tslib_1.__importDefault(require("./releaseListDropdown"));
var utils_1 = require("./utils");
var displayOptions = (_a = {},
    _a[utils_1.DisplayOption.SESSIONS] = locale_1.t('Sessions'),
    _a[utils_1.DisplayOption.USERS] = locale_1.t('Users'),
    _a);
function ReleaseListDisplayOptions(_a) {
    var selected = _a.selected, onSelect = _a.onSelect;
    return (<StyledReleaseListDropdown label={locale_1.t('Display')} options={displayOptions} selected={selected} onSelect={onSelect}/>);
}
exports.default = ReleaseListDisplayOptions;
var StyledReleaseListDropdown = styled_1.default(releaseListDropdown_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  z-index: 1;\n  @media (max-width: ", ") {\n    order: 3;\n  }\n"], ["\n  z-index: 1;\n  @media (max-width: ", ") {\n    order: 3;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var templateObject_1;
//# sourceMappingURL=releaseDisplayOptions.jsx.map