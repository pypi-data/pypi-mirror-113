Object.defineProperty(exports, "__esModule", { value: true });
exports.GridResizer = exports.GridBodyCellStatus = exports.GridBodyCell = exports.GridBody = exports.GridHeadCellStatic = exports.GridHeadCell = exports.GridHead = exports.GridRow = exports.Grid = exports.Body = exports.HeaderButtonContainer = exports.HeaderTitle = exports.Header = exports.GRID_STATUS_MESSAGE_HEIGHT = exports.GRID_BODY_ROW_HEIGHT = exports.GRID_HEAD_ROW_HEIGHT = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var panels_1 = require("app/components/panels");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
exports.GRID_HEAD_ROW_HEIGHT = 45;
exports.GRID_BODY_ROW_HEIGHT = 40;
exports.GRID_STATUS_MESSAGE_HEIGHT = exports.GRID_BODY_ROW_HEIGHT * 4;
/**
 * Local z-index stacking context
 * https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Positioning/Understanding_z_index/The_stacking_context
 */
// Parent context is Panel
var Z_INDEX_PANEL = 1;
var Z_INDEX_GRID_STATUS = -1;
var Z_INDEX_GRID = 5;
// Parent context is GridHeadCell
var Z_INDEX_GRID_RESIZER = 1;
exports.Header = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin-bottom: ", ";\n"])), space_1.default(1));
exports.HeaderTitle = styled_1.default('h4')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n  font-size: ", ";\n  color: ", ";\n"], ["\n  margin: 0;\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.subText; });
exports.HeaderButtonContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n  grid-auto-columns: auto;\n  justify-items: end;\n\n  /* Hovercard anchor element when features are disabled. */\n  & > span {\n    display: flex;\n    flex-direction: row;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n  grid-auto-columns: auto;\n  justify-items: end;\n\n  /* Hovercard anchor element when features are disabled. */\n  & > span {\n    display: flex;\n    flex-direction: row;\n  }\n"])), space_1.default(1));
var PanelWithProtectedBorder = styled_1.default(panels_1.Panel)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  z-index: ", ";\n"], ["\n  overflow: hidden;\n  z-index: ", ";\n"])), Z_INDEX_PANEL);
var Body = function (props) { return (<PanelWithProtectedBorder>
    <panels_1.PanelBody>{props.children}</panels_1.PanelBody>
  </PanelWithProtectedBorder>); };
exports.Body = Body;
/**
 * Grid is the parent element for the tableResizable component.
 *
 * On newer browsers, it will use CSS Grids to implement its layout.
 *
 * However, it is based on <table>, which has a distinction between header/body
 * HTML elements, which allows CSS selectors to its full potential. This has
 * the added advantage that older browsers will still have a chance of
 * displaying the data correctly (but this is untested).
 *
 * <thead>, <tbody>, <tr> are ignored by CSS Grid.
 * The entire layout is determined by the usage of <th> and <td>.
 */
exports.Grid = styled_1.default('table')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  position: inherit;\n  display: grid;\n\n  /* Overwritten by GridEditable.setGridTemplateColumns */\n  grid-template-columns: repeat(auto-fill, minmax(50px, auto));\n\n  box-sizing: border-box;\n  border-collapse: collapse;\n  margin: 0;\n\n  z-index: ", ";\n  overflow-x: auto;\n"], ["\n  position: inherit;\n  display: grid;\n\n  /* Overwritten by GridEditable.setGridTemplateColumns */\n  grid-template-columns: repeat(auto-fill, minmax(50px, auto));\n\n  box-sizing: border-box;\n  border-collapse: collapse;\n  margin: 0;\n\n  z-index: ", ";\n  overflow-x: auto;\n"])), Z_INDEX_GRID);
exports.GridRow = styled_1.default('tr')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: contents;\n\n  &:last-child,\n  &:last-child > td:first-child,\n  &:last-child > td:last-child {\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n"], ["\n  display: contents;\n\n  &:last-child,\n  &:last-child > td:first-child,\n  &:last-child > td:last-child {\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n"])), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; });
/**
 * GridHead is the collection of elements that builds the header section of the
 * Grid. As the entirety of the add/remove/resize actions are performed on the
 * header, most of the elements behave different for each stage.
 */
exports.GridHead = styled_1.default('thead')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: contents;\n"], ["\n  display: contents;\n"])));
exports.GridHeadCell = styled_1.default('th')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  /* By default, a grid item cannot be smaller than the size of its content.\n     We override this by setting min-width to be 0. */\n  position: relative; /* Used by GridResizer */\n  height: ", "px;\n  display: flex;\n  align-items: center;\n  min-width: 24px;\n  padding: 0 ", ";\n\n  border-right: 1px solid transparent;\n  border-left: 1px solid transparent;\n  background-color: ", ";\n  color: ", ";\n\n  font-size: ", ";\n  font-weight: 600;\n  text-transform: uppercase;\n  user-select: none;\n\n  a,\n  div,\n  span {\n    line-height: 1.1;\n    color: inherit;\n    white-space: nowrap;\n    text-overflow: ellipsis;\n    overflow: hidden;\n  }\n\n  &:first-child {\n    border-top-left-radius: ", ";\n  }\n\n  &:last-child {\n    border-top-right-radius: ", ";\n    border-right: none;\n  }\n\n  &:hover {\n    border-left-color: ", ";\n    border-right-color: ", ";\n  }\n"], ["\n  /* By default, a grid item cannot be smaller than the size of its content.\n     We override this by setting min-width to be 0. */\n  position: relative; /* Used by GridResizer */\n  height: ", "px;\n  display: flex;\n  align-items: center;\n  min-width: 24px;\n  padding: 0 ", ";\n\n  border-right: 1px solid transparent;\n  border-left: 1px solid transparent;\n  background-color: ", ";\n  color: ", ";\n\n  font-size: ", ";\n  font-weight: 600;\n  text-transform: uppercase;\n  user-select: none;\n\n  a,\n  div,\n  span {\n    line-height: 1.1;\n    color: inherit;\n    white-space: nowrap;\n    text-overflow: ellipsis;\n    overflow: hidden;\n  }\n\n  &:first-child {\n    border-top-left-radius: ", ";\n  }\n\n  &:last-child {\n    border-top-right-radius: ", ";\n    border-right: none;\n  }\n\n  &:hover {\n    border-left-color: ", ";\n    border-right-color: ", ";\n  }\n"])), exports.GRID_HEAD_ROW_HEIGHT, space_1.default(2), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return (p.isFirst ? 'transparent' : p.theme.border); }, function (p) { return p.theme.border; });
/**
 * Create spacing/padding similar to GridHeadCellWrapper but
 * without interactive aspects.
 */
exports.GridHeadCellStatic = styled_1.default('th')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  height: ", "px;\n  display: flex;\n  align-items: center;\n  padding: 0 ", ";\n  background-color: ", ";\n  font-size: ", ";\n  font-weight: 600;\n  line-height: 1;\n  text-transform: uppercase;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n  overflow: hidden;\n\n  &:first-child {\n    border-top-left-radius: ", ";\n    padding: ", " 0 ", " ", ";\n  }\n"], ["\n  height: ", "px;\n  display: flex;\n  align-items: center;\n  padding: 0 ", ";\n  background-color: ", ";\n  font-size: ", ";\n  font-weight: 600;\n  line-height: 1;\n  text-transform: uppercase;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n  overflow: hidden;\n\n  &:first-child {\n    border-top-left-radius: ", ";\n    padding: ", " 0 ", " ", ";\n  }\n"])), exports.GRID_HEAD_ROW_HEIGHT, space_1.default(2), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.borderRadius; }, space_1.default(1), space_1.default(1), space_1.default(3));
/**
 * GridBody are the collection of elements that contains and display the data
 * of the Grid. They are rather simple.
 */
exports.GridBody = styled_1.default('tbody')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  display: contents;\n\n  > tr:first-child td {\n    border-top: 1px solid ", ";\n  }\n"], ["\n  display: contents;\n\n  > tr:first-child td {\n    border-top: 1px solid ", ";\n  }\n"])), function (p) { return p.theme.border; });
exports.GridBodyCell = styled_1.default('td')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  /* By default, a grid item cannot be smaller than the size of its content.\n     We override this by setting min-width to be 0. */\n  min-width: 0;\n  /* Locking in the height makes calculation for resizer to be easier.\n     min-height is used to allow a cell to expand and this is used to display\n     feedback during empty/error state */\n  min-height: ", "px;\n  padding: ", " ", ";\n\n  background-color: ", ";\n  border-top: 1px solid ", ";\n\n  font-size: ", ";\n\n  &:first-child {\n    padding: ", " 0 ", " ", ";\n  }\n\n  &:last-child {\n    border-right: none;\n  }\n"], ["\n  /* By default, a grid item cannot be smaller than the size of its content.\n     We override this by setting min-width to be 0. */\n  min-width: 0;\n  /* Locking in the height makes calculation for resizer to be easier.\n     min-height is used to allow a cell to expand and this is used to display\n     feedback during empty/error state */\n  min-height: ", "px;\n  padding: ", " ", ";\n\n  background-color: ", ";\n  border-top: 1px solid ", ";\n\n  font-size: ", ";\n\n  &:first-child {\n    padding: ", " 0 ", " ", ";\n  }\n\n  &:last-child {\n    border-right: none;\n  }\n"])), exports.GRID_BODY_ROW_HEIGHT, space_1.default(1), space_1.default(2), function (p) { return p.theme.background; }, function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.fontSizeMedium; }, space_1.default(1), space_1.default(1), space_1.default(3));
var GridStatusWrapper = styled_1.default(exports.GridBodyCell)(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  grid-column: 1 / -1;\n  width: 100%;\n  height: ", "px;\n  background-color: transparent;\n"], ["\n  grid-column: 1 / -1;\n  width: 100%;\n  height: ", "px;\n  background-color: transparent;\n"])), exports.GRID_STATUS_MESSAGE_HEIGHT);
var GridStatusFloat = styled_1.default('div')(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 45px;\n  left: 0;\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  width: 100%;\n  height: ", "px;\n\n  z-index: ", ";\n  background: ", ";\n"], ["\n  position: absolute;\n  top: 45px;\n  left: 0;\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  width: 100%;\n  height: ", "px;\n\n  z-index: ", ";\n  background: ", ";\n"])), exports.GRID_STATUS_MESSAGE_HEIGHT, Z_INDEX_GRID_STATUS, function (p) { return p.theme.background; });
var GridBodyCellStatus = function (props) { return (<GridStatusWrapper>
    <GridStatusFloat>{props.children}</GridStatusFloat>
  </GridStatusWrapper>); };
exports.GridBodyCellStatus = GridBodyCellStatus;
/**
 * We have a fat GridResizer and we use the ::after pseudo-element to draw
 * a thin 1px border.
 *
 * The right most cell does not have a resizer as resizing from that side does strange things.
 */
exports.GridResizer = styled_1.default('div')(templateObject_14 || (templateObject_14 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 0px;\n  right: -6px;\n  width: 11px;\n\n  height: ", "px;\n\n  padding-left: 5px;\n  padding-right: 5px;\n\n  cursor: col-resize;\n  z-index: ", ";\n\n  /**\n   * This element allows us to have a fat GridResizer that is easy to hover and\n   * drag, but still draws an appealing thin line for the border\n   */\n  &::after {\n    content: ' ';\n    display: block;\n    width: 100%; /* Equivalent to 1px */\n    height: 100%;\n  }\n\n  &:hover::after {\n    background-color: ", ";\n  }\n\n  /**\n   * Ensure that this rule is after :hover, otherwise it will flicker when\n   * the GridResizer is dragged\n   */\n  &:active::after,\n  &:focus::after {\n    background-color: ", ";\n  }\n\n  /**\n   * This element gives the resize handle a more visible knob to grab\n   */\n  &:hover::before {\n    position: absolute;\n    top: 0;\n    left: 2px;\n    content: ' ';\n    display: block;\n    width: 7px;\n    height: ", "px;\n    background-color: ", ";\n    opacity: 0.4;\n  }\n"], ["\n  position: absolute;\n  top: 0px;\n  right: -6px;\n  width: 11px;\n\n  height: ", "px;\n\n  padding-left: 5px;\n  padding-right: 5px;\n\n  cursor: col-resize;\n  z-index: ", ";\n\n  /**\n   * This element allows us to have a fat GridResizer that is easy to hover and\n   * drag, but still draws an appealing thin line for the border\n   */\n  &::after {\n    content: ' ';\n    display: block;\n    width: 100%; /* Equivalent to 1px */\n    height: 100%;\n  }\n\n  &:hover::after {\n    background-color: ", ";\n  }\n\n  /**\n   * Ensure that this rule is after :hover, otherwise it will flicker when\n   * the GridResizer is dragged\n   */\n  &:active::after,\n  &:focus::after {\n    background-color: ", ";\n  }\n\n  /**\n   * This element gives the resize handle a more visible knob to grab\n   */\n  &:hover::before {\n    position: absolute;\n    top: 0;\n    left: 2px;\n    content: ' ';\n    display: block;\n    width: 7px;\n    height: ", "px;\n    background-color: ", ";\n    opacity: 0.4;\n  }\n"])), function (p) {
    var numOfRows = p.dataRows;
    var height = exports.GRID_HEAD_ROW_HEIGHT + numOfRows * exports.GRID_BODY_ROW_HEIGHT;
    if (numOfRows >= 2) {
        // account for border-bottom height
        height += numOfRows - 1;
    }
    return height;
}, Z_INDEX_GRID_RESIZER, function (p) { return p.theme.gray200; }, function (p) { return p.theme.purple300; }, exports.GRID_HEAD_ROW_HEIGHT, function (p) { return p.theme.purple300; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14;
//# sourceMappingURL=styles.jsx.map