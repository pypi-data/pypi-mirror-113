Object.defineProperty(exports, "__esModule", { value: true });
exports.PanelTableHeader = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var is_prop_valid_1 = tslib_1.__importDefault(require("@emotion/is-prop-valid"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var panel_1 = tslib_1.__importDefault(require("./panel"));
/**
 * Bare bones table generates a CSS grid template based on the content.
 *
 * The number of children elements should be a multiple of `this.props.columns` to have
 * it look ok.
 *
 *
 * Potential customizations:
 * - [ ] Add borders for columns to make them more like cells
 * - [ ] Add prop to disable borders for rows
 * - [ ] We may need to wrap `children` with our own component (similar to what we're doing
 *       with `headers`. Then we can get rid of that gross `> *` selector
 * - [ ] Allow customization of wrappers (Header and body cells if added)
 */
var PanelTable = function (_a) {
    var headers = _a.headers, children = _a.children, isLoading = _a.isLoading, isEmpty = _a.isEmpty, disablePadding = _a.disablePadding, className = _a.className, _b = _a.emptyMessage, emptyMessage = _b === void 0 ? locale_1.t('There are no items to display') : _b, emptyAction = _a.emptyAction, loader = _a.loader;
    var shouldShowLoading = isLoading === true;
    var shouldShowEmptyMessage = !shouldShowLoading && isEmpty;
    var shouldShowContent = !shouldShowLoading && !shouldShowEmptyMessage;
    return (<Wrapper columns={headers.length} disablePadding={disablePadding} className={className} hasRows={shouldShowContent}>
      {headers.map(function (header, i) { return (<exports.PanelTableHeader key={i}>{header}</exports.PanelTableHeader>); })}

      {shouldShowLoading && (<LoadingWrapper>{loader || <loadingIndicator_1.default />}</LoadingWrapper>)}

      {shouldShowEmptyMessage && (<TableEmptyStateWarning>
          <p>{emptyMessage}</p>
          {emptyAction}
        </TableEmptyStateWarning>)}

      {shouldShowContent && getContent(children)}
    </Wrapper>);
};
function getContent(children) {
    if (typeof children === 'function') {
        return children();
    }
    return children;
}
var LoadingWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject([""], [""])));
var TableEmptyStateWarning = styled_1.default(emptyStateWarning_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject([""], [""])));
var Wrapper = styled_1.default(panel_1.default, {
    shouldForwardProp: function (p) { return typeof p === 'string' && is_prop_valid_1.default(p) && p !== 'columns'; },
})(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(", ", auto);\n\n  > * {\n    ", "\n\n    &:nth-last-child(n + ", ") {\n      border-bottom: 1px solid ", ";\n    }\n  }\n\n  > ", ", > ", " {\n    border: none;\n    grid-column: auto / span ", ";\n  }\n\n  /* safari needs an overflow value or the contents will spill out */\n  overflow: auto;\n"], ["\n  display: grid;\n  grid-template-columns: repeat(", ", auto);\n\n  > * {\n    ", "\n\n    &:nth-last-child(n + ", ") {\n      border-bottom: 1px solid ", ";\n    }\n  }\n\n  > " /* sc-selector */, ", > " /* sc-selector */, " {\n    border: none;\n    grid-column: auto / span ", ";\n  }\n\n  /* safari needs an overflow value or the contents will spill out */\n  overflow: auto;\n"])), function (p) { return p.columns; }, function (p) { return (p.disablePadding ? '' : "padding: " + space_1.default(2) + ";"); }, function (p) { return (p.hasRows ? p.columns + 1 : 0); }, function (p) { return p.theme.border; }, /* sc-selector */ TableEmptyStateWarning, /* sc-selector */ LoadingWrapper, function (p) { return p.columns; });
exports.PanelTableHeader = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  font-weight: 600;\n  text-transform: uppercase;\n  border-radius: ", " ", " 0 0;\n  background: ", ";\n  line-height: 1;\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  min-height: 45px;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  font-weight: 600;\n  text-transform: uppercase;\n  border-radius: ", " ", " 0 0;\n  background: ", ";\n  line-height: 1;\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  min-height: 45px;\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.backgroundSecondary; });
exports.default = PanelTable;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=panelTable.jsx.map