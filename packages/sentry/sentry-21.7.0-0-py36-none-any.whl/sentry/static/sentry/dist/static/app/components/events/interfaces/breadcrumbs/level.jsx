Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var highlight_1 = tslib_1.__importDefault(require("app/components/highlight"));
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var locale_1 = require("app/locale");
var breadcrumbs_1 = require("app/types/breadcrumbs");
var Level = react_1.memo(function (_a) {
    var level = _a.level, _b = _a.searchTerm, searchTerm = _b === void 0 ? '' : _b;
    switch (level) {
        case breadcrumbs_1.BreadcrumbLevelType.FATAL:
            return (<tag_1.default type="error">
          <highlight_1.default text={searchTerm}>{locale_1.t('fatal')}</highlight_1.default>
        </tag_1.default>);
        case breadcrumbs_1.BreadcrumbLevelType.ERROR:
            return (<tag_1.default type="error">
          <highlight_1.default text={searchTerm}>{locale_1.t('error')}</highlight_1.default>
        </tag_1.default>);
        case breadcrumbs_1.BreadcrumbLevelType.INFO:
            return (<tag_1.default type="info">
          <highlight_1.default text={searchTerm}>{locale_1.t('info')}</highlight_1.default>
        </tag_1.default>);
        case breadcrumbs_1.BreadcrumbLevelType.WARNING:
            return (<tag_1.default type="warning">
          <highlight_1.default text={searchTerm}>{locale_1.t('warning')}</highlight_1.default>
        </tag_1.default>);
        default:
            return (<tag_1.default>
          <highlight_1.default text={searchTerm}>{level || locale_1.t('undefined')}</highlight_1.default>
        </tag_1.default>);
    }
});
exports.default = Level;
//# sourceMappingURL=level.jsx.map