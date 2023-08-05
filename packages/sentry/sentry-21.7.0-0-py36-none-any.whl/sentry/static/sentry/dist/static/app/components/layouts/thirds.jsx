Object.defineProperty(exports, "__esModule", { value: true });
exports.Side = exports.Main = exports.HeaderNavTabs = exports.Header = exports.Title = exports.HeaderActions = exports.HeaderContent = exports.Body = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var navTabs_1 = tslib_1.__importDefault(require("app/components/navTabs"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
/**
 * Base container for 66/33 containers.
 */
exports.Body = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  margin: 0;\n  background-color: ", ";\n  flex-grow: 1;\n\n  @media (min-width: ", ") {\n    padding: ", " ", ";\n  }\n\n  @media (min-width: ", ") {\n    display: grid;\n    grid-template-columns: 66% auto;\n    align-content: start;\n    grid-gap: ", ";\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(100px, auto) 325px;\n  }\n"], ["\n  padding: ", ";\n  margin: 0;\n  background-color: ", ";\n  flex-grow: 1;\n\n  @media (min-width: ", ") {\n    padding: ", " ", ";\n  }\n\n  @media (min-width: ", ") {\n    display: grid;\n    grid-template-columns: 66% auto;\n    align-content: start;\n    grid-gap: ", ";\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(100px, auto) 325px;\n  }\n"])), space_1.default(2), function (p) { return p.theme.background; }, function (p) { return p.theme.breakpoints[0]; }, space_1.default(3), space_1.default(4), function (p) { return p.theme.breakpoints[1]; }, space_1.default(3), function (p) { return p.theme.breakpoints[2]; });
/**
 * Use HeaderContent to create horizontal regions in the header
 * that contain a heading/breadcrumbs and a button group.
 */
exports.HeaderContent = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  justify-content: normal;\n  margin-bottom: ", ";\n  overflow: hidden;\n  max-width: 100%;\n\n  @media (max-width: ", ") {\n    margin-bottom: ", ";\n  }\n"], ["\n  display: flex;\n  flex-direction: column;\n  justify-content: normal;\n  margin-bottom: ", ";\n  overflow: hidden;\n  max-width: 100%;\n\n  @media (max-width: ", ") {\n    margin-bottom: ", ";\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[1]; }, space_1.default(1));
/**
 * Container for action buttons and secondary information that
 * flows on the top right of the header.
 */
exports.HeaderActions = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  justify-content: normal;\n  min-width: max-content;\n\n  @media (max-width: ", ") {\n    width: max-content;\n    margin-bottom: ", ";\n  }\n"], ["\n  display: flex;\n  flex-direction: column;\n  justify-content: normal;\n  min-width: max-content;\n\n  @media (max-width: ", ") {\n    width: max-content;\n    margin-bottom: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[1]; }, space_1.default(2));
/**
 * Heading container that includes margins.
 */
exports.Title = styled_1.default('h2')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  font-weight: normal;\n  line-height: 1.2;\n  color: ", ";\n  margin-top: ", ";\n  /* TODO(bootstrap) Remove important when bootstrap headings are removed */\n  margin-bottom: 0 !important;\n  min-height: 30px;\n  align-self: center;\n  ", ";\n\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"], ["\n  font-size: ", ";\n  font-weight: normal;\n  line-height: 1.2;\n  color: ", ";\n  margin-top: ", ";\n  /* TODO(bootstrap) Remove important when bootstrap headings are removed */\n  margin-bottom: 0 !important;\n  min-height: 30px;\n  align-self: center;\n  ", ";\n\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"])), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.textColor; }, space_1.default(3), overflowEllipsis_1.default, function (p) { return p.theme.breakpoints[1]; }, space_1.default(1));
/**
 * Header container for header content and header actions.
 *
 * Uses a horizontal layout in wide viewports to put space between
 * the headings and the actions container. In narrow viewports these elements
 * are stacked vertically.
 */
exports.Header = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(0, 1fr);\n  padding: ", " ", " 0 ", ";\n  background-color: transparent;\n  border-bottom: 1px solid ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(0, 1fr) auto;\n    padding: ", " ", " 0 ", ";\n  }\n"], ["\n  display: grid;\n  grid-template-columns: minmax(0, 1fr);\n  padding: ", " ", " 0 ", ";\n  background-color: transparent;\n  border-bottom: 1px solid ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(0, 1fr) auto;\n    padding: ", " ", " 0 ", ";\n  }\n"])), space_1.default(2), space_1.default(2), space_1.default(2), function (p) { return p.theme.border; }, function (p) { return p.theme.breakpoints[1]; }, space_1.default(2), space_1.default(4), space_1.default(4));
/**
 * Styled Nav Tabs for use inside a Layout.Header component
 */
exports.HeaderNavTabs = styled_1.default(navTabs_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n  border-bottom: 0 !important;\n\n  & > li {\n    margin-right: ", ";\n  }\n  & > li > a {\n    padding: ", " 0;\n    font-size: ", ";\n    margin-bottom: 4px;\n  }\n  & > li.active > a {\n    margin-bottom: 0;\n  }\n"], ["\n  margin: 0;\n  border-bottom: 0 !important;\n\n  & > li {\n    margin-right: ", ";\n  }\n  & > li > a {\n    padding: ", " 0;\n    font-size: ", ";\n    margin-bottom: 4px;\n  }\n  & > li.active > a {\n    margin-bottom: 0;\n  }\n"])), space_1.default(3), space_1.default(1), function (p) { return p.theme.fontSizeLarge; });
/**
 * Containers for two column 66/33 layout.
 */
exports.Main = styled_1.default('section')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  grid-column: ", ";\n  max-width: 100%;\n"], ["\n  grid-column: ", ";\n  max-width: 100%;\n"])), function (p) { return (p.fullWidth ? '1/3' : '1/2'); });
exports.Side = styled_1.default('aside')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  grid-column: 2/3;\n"], ["\n  grid-column: 2/3;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=thirds.jsx.map