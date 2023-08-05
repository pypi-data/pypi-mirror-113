Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var breadcrumbs_1 = require("app/types/breadcrumbs");
var category_1 = tslib_1.__importDefault(require("./category"));
var data_1 = tslib_1.__importDefault(require("./data"));
var icon_1 = tslib_1.__importDefault(require("./icon"));
var level_1 = tslib_1.__importDefault(require("./level"));
var styles_1 = require("./styles");
var time_1 = tslib_1.__importDefault(require("./time"));
var ListBody = react_1.memo(function (_a) {
    var orgId = _a.orgId, event = _a.event, breadcrumb = _a.breadcrumb, relativeTime = _a.relativeTime, displayRelativeTime = _a.displayRelativeTime, searchTerm = _a.searchTerm, isLastItem = _a.isLastItem, height = _a.height;
    var hasError = breadcrumb.type === breadcrumbs_1.BreadcrumbType.ERROR;
    return (<react_1.Fragment>
        <styles_1.GridCellLeft hasError={hasError} isLastItem={isLastItem}>
          <tooltip_1.default title={breadcrumb.description}>
            <icon_1.default icon={breadcrumb.icon} color={breadcrumb.color}/>
          </tooltip_1.default>
        </styles_1.GridCellLeft>
        <GridCellCategory hasError={hasError} isLastItem={isLastItem}>
          <category_1.default category={breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.category} searchTerm={searchTerm}/>
        </GridCellCategory>
        <styles_1.GridCell hasError={hasError} isLastItem={isLastItem} height={height}>
          <data_1.default event={event} orgId={orgId} breadcrumb={breadcrumb} searchTerm={searchTerm}/>
        </styles_1.GridCell>
        <styles_1.GridCell hasError={hasError} isLastItem={isLastItem}>
          <level_1.default level={breadcrumb.level} searchTerm={searchTerm}/>
        </styles_1.GridCell>
        <styles_1.GridCell hasError={hasError} isLastItem={isLastItem}>
          <time_1.default timestamp={breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.timestamp} relativeTime={relativeTime} displayRelativeTime={displayRelativeTime} searchTerm={searchTerm}/>
        </styles_1.GridCell>
      </react_1.Fragment>);
});
exports.default = ListBody;
var GridCellCategory = styled_1.default(styles_1.GridCell)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    padding-left: ", ";\n  }\n"], ["\n  @media (min-width: ", ") {\n    padding-left: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space_1.default(1));
var templateObject_1;
//# sourceMappingURL=listBody.jsx.map