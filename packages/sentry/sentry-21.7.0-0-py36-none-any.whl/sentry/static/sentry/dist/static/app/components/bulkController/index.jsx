Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var intersection_1 = tslib_1.__importDefault(require("lodash/intersection"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var uniq_1 = tslib_1.__importDefault(require("lodash/uniq"));
var xor_1 = tslib_1.__importDefault(require("lodash/xor"));
var bulkNotice_1 = tslib_1.__importDefault(require("./bulkNotice"));
var BulkController = /** @class */ (function (_super) {
    tslib_1.__extends(BulkController, _super);
    function BulkController() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.handleRowToggle = function (id) {
            _this.setState(function (state) { return ({
                selectedIds: xor_1.default(state.selectedIds, [id]),
                isAllSelected: false,
            }); });
        };
        _this.handleAllRowsToggle = function (select) {
            var pageIds = _this.props.pageIds;
            _this.setState({
                selectedIds: select ? tslib_1.__spreadArray([], tslib_1.__read(pageIds)) : [],
                isAllSelected: select,
            });
        };
        _this.handlePageRowsToggle = function (select) {
            var pageIds = _this.props.pageIds;
            _this.setState(function (state) { return ({
                selectedIds: select
                    ? uniq_1.default(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(state.selectedIds)), tslib_1.__read(pageIds)))
                    : state.selectedIds.filter(function (id) { return !pageIds.includes(id); }),
                isAllSelected: false,
            }); });
        };
        return _this;
    }
    BulkController.prototype.getInitialState = function () {
        var _a = this.props, defaultSelectedIds = _a.defaultSelectedIds, pageIds = _a.pageIds;
        return {
            selectedIds: intersection_1.default(defaultSelectedIds !== null && defaultSelectedIds !== void 0 ? defaultSelectedIds : [], pageIds),
            isAllSelected: false,
        };
    };
    BulkController.getDerivedStateFromProps = function (props, state) {
        return tslib_1.__assign(tslib_1.__assign({}, state), { selectedIds: intersection_1.default(state.selectedIds, props.pageIds) });
    };
    BulkController.prototype.componentDidUpdate = function (_prevProps, prevState) {
        var _a, _b;
        if (!isEqual_1.default(prevState, this.state)) {
            (_b = (_a = this.props).onChange) === null || _b === void 0 ? void 0 : _b.call(_a, this.state);
        }
    };
    BulkController.prototype.render = function () {
        var _this = this;
        var _a = this.props, pageIds = _a.pageIds, children = _a.children, columnsCount = _a.columnsCount, allRowsCount = _a.allRowsCount, bulkLimit = _a.bulkLimit;
        var _b = this.state, selectedIds = _b.selectedIds, isAllSelected = _b.isAllSelected;
        var isPageSelected = pageIds.length > 0 && pageIds.every(function (id) { return selectedIds.includes(id); });
        var renderProps = {
            selectedIds: selectedIds,
            isAllSelected: isAllSelected,
            isPageSelected: isPageSelected,
            onRowToggle: this.handleRowToggle,
            onAllRowsToggle: this.handleAllRowsToggle,
            onPageRowsToggle: this.handlePageRowsToggle,
            renderBulkNotice: function () { return (<bulkNotice_1.default allRowsCount={allRowsCount} selectedRowsCount={selectedIds.length} onUnselectAllRows={function () { return _this.handleAllRowsToggle(false); }} onSelectAllRows={function () { return _this.handleAllRowsToggle(true); }} columnsCount={columnsCount} isPageSelected={isPageSelected} isAllSelected={isAllSelected} bulkLimit={bulkLimit}/>); },
        };
        return children(renderProps);
    };
    return BulkController;
}(React.Component));
exports.default = BulkController;
//# sourceMappingURL=index.jsx.map