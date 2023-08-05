Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var globalSelectionLink_1 = tslib_1.__importDefault(require("app/components/globalSelectionLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var icons_1 = require("app/icons");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var breadcrumbDropdown_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsBreadcrumb/breadcrumbDropdown"));
var BreadcrumbList = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", " 0;\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", " 0;\n"])), space_1.default(1));
function isCrumbDropdown(crumb) {
    return crumb.items !== undefined;
}
/**
 * Page breadcrumbs used for navigation, not to be confused with sentry's event breadcrumbs
 */
var Breadcrumbs = function (_a) {
    var crumbs = _a.crumbs, _b = _a.linkLastItem, linkLastItem = _b === void 0 ? false : _b, props = tslib_1.__rest(_a, ["crumbs", "linkLastItem"]);
    if (crumbs.length === 0) {
        return null;
    }
    if (!linkLastItem) {
        var lastCrumb = crumbs[crumbs.length - 1];
        if (!isCrumbDropdown(lastCrumb)) {
            lastCrumb.to = null;
        }
    }
    return (<BreadcrumbList {...props}>
      {crumbs.map(function (crumb, index) {
            if (isCrumbDropdown(crumb)) {
                var label = crumb.label, crumbProps = tslib_1.__rest(crumb, ["label"]);
                return (<breadcrumbDropdown_1.default key={index} isLast={index >= crumbs.length - 1} route={{}} name={label} {...crumbProps}/>);
            }
            else {
                var label = crumb.label, to = crumb.to, preserveGlobalSelection = crumb.preserveGlobalSelection, key = crumb.key;
                var labelKey = typeof label === 'string' ? label : '';
                var mapKey = (key !== null && key !== void 0 ? key : typeof to === 'string') ? "" + labelKey + to : "" + labelKey + index;
                return (<React.Fragment key={mapKey}>
              {to ? (<BreadcrumbLink to={to} preserveGlobalSelection={preserveGlobalSelection}>
                  {label}
                </BreadcrumbLink>) : (<BreadcrumbItem>{label}</BreadcrumbItem>)}

              {index < crumbs.length - 1 && (<BreadcrumbDividerIcon size="xs" direction="right"/>)}
            </React.Fragment>);
            }
        })}
    </BreadcrumbList>);
};
var getBreadcrumbListItemStyles = function (p) { return "\n  color: " + p.theme.gray300 + ";\n  " + overflowEllipsis_1.default + ";\n  width: auto;\n\n  &:last-child {\n    color: " + p.theme.textColor + ";\n  }\n"; };
var BreadcrumbLink = styled_1.default(function (_a) {
    var preserveGlobalSelection = _a.preserveGlobalSelection, to = _a.to, props = tslib_1.__rest(_a, ["preserveGlobalSelection", "to"]);
    return preserveGlobalSelection ? (<globalSelectionLink_1.default to={to} {...props}/>) : (<link_1.default to={to} {...props}/>);
})(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", "\n\n  &:hover,\n  &:active {\n    color: ", ";\n  }\n"], ["\n  ", "\n\n  &:hover,\n  &:active {\n    color: ", ";\n  }\n"])), getBreadcrumbListItemStyles, function (p) { return p.theme.subText; });
var BreadcrumbItem = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ", "\n  max-width: 400px;\n"], ["\n  ", "\n  max-width: 400px;\n"])), getBreadcrumbListItemStyles);
var BreadcrumbDividerIcon = styled_1.default(icons_1.IconChevron)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin: 0 ", ";\n  flex-shrink: 0;\n"], ["\n  color: ", ";\n  margin: 0 ", ";\n  flex-shrink: 0;\n"])), function (p) { return p.theme.gray300; }, space_1.default(1));
exports.default = Breadcrumbs;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=breadcrumbs.jsx.map