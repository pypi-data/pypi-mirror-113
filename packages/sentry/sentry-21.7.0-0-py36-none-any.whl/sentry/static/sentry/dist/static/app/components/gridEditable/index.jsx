Object.defineProperty(exports, "__esModule", { value: true });
exports.COL_WIDTH_MINIMUM = exports.COL_WIDTH_UNDEFINED = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var styles_1 = require("./styles");
// Auto layout width.
exports.COL_WIDTH_UNDEFINED = -1;
// Set to 90 as the edit/trash icons need this much space.
exports.COL_WIDTH_MINIMUM = 90;
var GridEditable = /** @class */ (function (_super) {
    tslib_1.__extends(GridEditable, _super);
    function GridEditable() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            numColumn: 0,
        };
        _this.refGrid = React.createRef();
        _this.resizeWindowLifecycleEvents = {
            mousemove: [],
            mouseup: [],
        };
        _this.onResetColumnSize = function (e, i) {
            e.stopPropagation();
            var nextColumnOrder = tslib_1.__spreadArray([], tslib_1.__read(_this.props.columnOrder));
            nextColumnOrder[i] = tslib_1.__assign(tslib_1.__assign({}, nextColumnOrder[i]), { width: exports.COL_WIDTH_UNDEFINED });
            _this.setGridTemplateColumns(nextColumnOrder);
            var onResizeColumn = _this.props.grid.onResizeColumn;
            if (onResizeColumn) {
                onResizeColumn(i, tslib_1.__assign(tslib_1.__assign({}, nextColumnOrder[i]), { width: exports.COL_WIDTH_UNDEFINED }));
            }
        };
        _this.onResizeMouseDown = function (e, i) {
            if (i === void 0) { i = -1; }
            e.stopPropagation();
            // Block right-click and other funky stuff
            if (i === -1 || e.type === 'contextmenu') {
                return;
            }
            // <GridResizer> is nested 1 level down from <GridHeadCell>
            var cell = e.currentTarget.parentElement;
            if (!cell) {
                return;
            }
            // HACK: Do not put into state to prevent re-rendering of component
            _this.resizeMetadata = {
                columnIndex: i,
                columnWidth: cell.offsetWidth,
                cursorX: e.clientX,
            };
            window.addEventListener('mousemove', _this.onResizeMouseMove);
            _this.resizeWindowLifecycleEvents.mousemove.push(_this.onResizeMouseMove);
            window.addEventListener('mouseup', _this.onResizeMouseUp);
            _this.resizeWindowLifecycleEvents.mouseup.push(_this.onResizeMouseUp);
        };
        _this.onResizeMouseUp = function (e) {
            var metadata = _this.resizeMetadata;
            var onResizeColumn = _this.props.grid.onResizeColumn;
            if (!metadata || !onResizeColumn) {
                return;
            }
            var columnOrder = _this.props.columnOrder;
            var widthChange = e.clientX - metadata.cursorX;
            onResizeColumn(metadata.columnIndex, tslib_1.__assign(tslib_1.__assign({}, columnOrder[metadata.columnIndex]), { width: metadata.columnWidth + widthChange }));
            _this.resizeMetadata = undefined;
            _this.clearWindowLifecycleEvents();
        };
        _this.onResizeMouseMove = function (e) {
            var resizeMetadata = _this.resizeMetadata;
            if (!resizeMetadata) {
                return;
            }
            window.requestAnimationFrame(function () { return _this.resizeGridColumn(e, resizeMetadata); });
        };
        /**
         * Recalculate the dimensions of Grid and Columns and redraws them
         */
        _this.redrawGridColumn = function () {
            _this.setGridTemplateColumns(_this.props.columnOrder);
        };
        _this.renderGridBodyRow = function (dataRow, row) {
            var _a = _this.props, columnOrder = _a.columnOrder, grid = _a.grid;
            var prependColumns = grid.renderPrependColumns
                ? grid.renderPrependColumns(false, dataRow, row)
                : [];
            return (<styles_1.GridRow key={row}>
        {prependColumns &&
                    prependColumns.map(function (item, i) { return (<styles_1.GridBodyCell key={"prepend-" + i}>{item}</styles_1.GridBodyCell>); })}
        {columnOrder.map(function (col, i) { return (<styles_1.GridBodyCell key={"" + col.key + i}>
            {grid.renderBodyCell
                        ? grid.renderBodyCell(col, dataRow, row, i)
                        : dataRow[col.key]}
          </styles_1.GridBodyCell>); })}
      </styles_1.GridRow>);
        };
        return _this;
    }
    // Static methods do not allow the use of generics bounded to the parent class
    // For more info: https://github.com/microsoft/TypeScript/issues/14600
    GridEditable.getDerivedStateFromProps = function (props, prevState) {
        return tslib_1.__assign(tslib_1.__assign({}, prevState), { numColumn: props.columnOrder.length });
    };
    GridEditable.prototype.componentDidMount = function () {
        window.addEventListener('resize', this.redrawGridColumn);
        this.setGridTemplateColumns(this.props.columnOrder);
    };
    GridEditable.prototype.componentDidUpdate = function () {
        // Redraw columns whenever new props are received
        this.setGridTemplateColumns(this.props.columnOrder);
    };
    GridEditable.prototype.componentWillUnmount = function () {
        this.clearWindowLifecycleEvents();
        window.removeEventListener('resize', this.redrawGridColumn);
    };
    GridEditable.prototype.clearWindowLifecycleEvents = function () {
        var _this = this;
        Object.keys(this.resizeWindowLifecycleEvents).forEach(function (e) {
            _this.resizeWindowLifecycleEvents[e].forEach(function (c) { return window.removeEventListener(e, c); });
            _this.resizeWindowLifecycleEvents[e] = [];
        });
    };
    GridEditable.prototype.resizeGridColumn = function (e, metadata) {
        var grid = this.refGrid.current;
        if (!grid) {
            return;
        }
        var widthChange = e.clientX - metadata.cursorX;
        var nextColumnOrder = tslib_1.__spreadArray([], tslib_1.__read(this.props.columnOrder));
        nextColumnOrder[metadata.columnIndex] = tslib_1.__assign(tslib_1.__assign({}, nextColumnOrder[metadata.columnIndex]), { width: Math.max(metadata.columnWidth + widthChange, 0) });
        this.setGridTemplateColumns(nextColumnOrder);
    };
    /**
     * Set the CSS for Grid Column
     */
    GridEditable.prototype.setGridTemplateColumns = function (columnOrder) {
        var grid = this.refGrid.current;
        if (!grid) {
            return;
        }
        var prependColumns = this.props.grid.prependColumnWidths || [];
        var prepend = prependColumns.join(' ');
        var widths = columnOrder.map(function (item, index) {
            if (item.width === exports.COL_WIDTH_UNDEFINED) {
                return "minmax(" + exports.COL_WIDTH_MINIMUM + "px, auto)";
            }
            else if (typeof item.width === 'number' && item.width > exports.COL_WIDTH_MINIMUM) {
                if (index === columnOrder.length - 1) {
                    return "minmax(" + item.width + "px, auto)";
                }
                return item.width + "px";
            }
            if (index === columnOrder.length - 1) {
                return "minmax(" + exports.COL_WIDTH_MINIMUM + "px, auto)";
            }
            return exports.COL_WIDTH_MINIMUM + "px";
        });
        // The last column has no resizer and should always be a flexible column
        // to prevent underflows.
        grid.style.gridTemplateColumns = prepend + " " + widths.join(' ');
    };
    GridEditable.prototype.renderGridHead = function () {
        var _this = this;
        var _a = this.props, error = _a.error, isLoading = _a.isLoading, columnOrder = _a.columnOrder, grid = _a.grid, data = _a.data;
        // Ensure that the last column cannot be removed
        var numColumn = columnOrder.length;
        var prependColumns = grid.renderPrependColumns
            ? grid.renderPrependColumns(true)
            : [];
        return (<styles_1.GridRow>
        {prependColumns &&
                prependColumns.map(function (item, i) { return (<styles_1.GridHeadCellStatic key={"prepend-" + i}>{item}</styles_1.GridHeadCellStatic>); })}
        {
            /* Note that this.onResizeMouseDown assumes GridResizer is nested
              1 levels under GridHeadCell */
            columnOrder.map(function (column, i) { return (<styles_1.GridHeadCell key={i + "." + column.key} isFirst={i === 0}>
              {grid.renderHeadCell ? grid.renderHeadCell(column, i) : column.name}
              {i !== numColumn - 1 && (<styles_1.GridResizer dataRows={!error && !isLoading && data ? data.length : 0} onMouseDown={function (e) { return _this.onResizeMouseDown(e, i); }} onDoubleClick={function (e) { return _this.onResetColumnSize(e, i); }} onContextMenu={_this.onResizeMouseDown}/>)}
            </styles_1.GridHeadCell>); })}
      </styles_1.GridRow>);
    };
    GridEditable.prototype.renderGridBody = function () {
        var _a = this.props, data = _a.data, error = _a.error, isLoading = _a.isLoading;
        if (error) {
            return this.renderError();
        }
        if (isLoading) {
            return this.renderLoading();
        }
        if (!data || data.length === 0) {
            return this.renderEmptyData();
        }
        return data.map(this.renderGridBodyRow);
    };
    GridEditable.prototype.renderError = function () {
        return (<styles_1.GridRow>
        <styles_1.GridBodyCellStatus>
          <icons_1.IconWarning color="gray300" size="lg"/>
        </styles_1.GridBodyCellStatus>
      </styles_1.GridRow>);
    };
    GridEditable.prototype.renderLoading = function () {
        return (<styles_1.GridRow>
        <styles_1.GridBodyCellStatus>
          <loadingIndicator_1.default />
        </styles_1.GridBodyCellStatus>
      </styles_1.GridRow>);
    };
    GridEditable.prototype.renderEmptyData = function () {
        return (<styles_1.GridRow>
        <styles_1.GridBodyCellStatus>
          <emptyStateWarning_1.default>
            <p>{locale_1.t('No results found for your query')}</p>
          </emptyStateWarning_1.default>
        </styles_1.GridBodyCellStatus>
      </styles_1.GridRow>);
    };
    GridEditable.prototype.render = function () {
        var _a = this.props, title = _a.title, headerButtons = _a.headerButtons;
        var showHeader = title || headerButtons;
        return (<React.Fragment>
        {showHeader && (<styles_1.Header>
            {title && <styles_1.HeaderTitle>{title}</styles_1.HeaderTitle>}
            {headerButtons && (<styles_1.HeaderButtonContainer>{headerButtons()}</styles_1.HeaderButtonContainer>)}
          </styles_1.Header>)}
        <styles_1.Body>
          <styles_1.Grid data-test-id="grid-editable" ref={this.refGrid}>
            <styles_1.GridHead>{this.renderGridHead()}</styles_1.GridHead>
            <styles_1.GridBody>{this.renderGridBody()}</styles_1.GridBody>
          </styles_1.Grid>
        </styles_1.Body>
      </React.Fragment>);
    };
    return GridEditable;
}(React.Component));
exports.default = GridEditable;
//# sourceMappingURL=index.jsx.map