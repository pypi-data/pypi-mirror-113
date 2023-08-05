Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var locale_1 = require("app/locale");
var releaseListDropdown_1 = tslib_1.__importDefault(require("./releaseListDropdown"));
var utils_1 = require("./utils");
function ReleaseListSortOptions(_a) {
    var _b, _c, _d;
    var selected = _a.selected, selectedDisplay = _a.selectedDisplay, onSelect = _a.onSelect, organization = _a.organization;
    var sortOptions = tslib_1.__assign((_b = {}, _b[utils_1.SortOption.DATE] = locale_1.t('Date Created'), _b[utils_1.SortOption.SESSIONS] = locale_1.t('Total Sessions'), _b), (selectedDisplay === utils_1.DisplayOption.USERS
        ? (_c = {},
            _c[utils_1.SortOption.USERS_24_HOURS] = locale_1.t('Active Users'),
            _c[utils_1.SortOption.CRASH_FREE_USERS] = locale_1.t('Crash Free Users'),
            _c) : (_d = {},
        _d[utils_1.SortOption.SESSIONS_24_HOURS] = locale_1.t('Active Sessions'),
        _d[utils_1.SortOption.CRASH_FREE_SESSIONS] = locale_1.t('Crash Free Sessions'),
        _d)));
    if (organization.features.includes('semver')) {
        sortOptions[utils_1.SortOption.BUILD] = locale_1.t('Build Number');
        sortOptions[utils_1.SortOption.SEMVER] = locale_1.t('Semantic Version');
    }
    if (organization.features.includes('release-adoption-stage')) {
        sortOptions[utils_1.SortOption.ADOPTION] = locale_1.t('Date Adopted');
    }
    return (<StyledReleaseListDropdown label={locale_1.t('Sort By')} options={sortOptions} selected={selected} onSelect={onSelect}/>);
}
exports.default = ReleaseListSortOptions;
var StyledReleaseListDropdown = styled_1.default(releaseListDropdown_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  z-index: 2;\n  @media (max-width: ", ") {\n    order: 2;\n  }\n"], ["\n  z-index: 2;\n  @media (max-width: ", ") {\n    order: 2;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var templateObject_1;
//# sourceMappingURL=releaseListSortOptions.jsx.map