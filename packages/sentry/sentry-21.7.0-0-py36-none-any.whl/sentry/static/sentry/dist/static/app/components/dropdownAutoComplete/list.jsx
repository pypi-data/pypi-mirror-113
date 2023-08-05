Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_virtualized_1 = require("react-virtualized");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var row_1 = tslib_1.__importDefault(require("./row"));
function getHeight(items, maxHeight, virtualizedHeight, virtualizedLabelHeight) {
    var minHeight = virtualizedLabelHeight
        ? items.reduce(function (a, r) { return a + (r.groupLabel ? virtualizedLabelHeight : virtualizedHeight); }, 0)
        : items.length * virtualizedHeight;
    return Math.min(minHeight, maxHeight);
}
var List = function (_a) {
    var virtualizedHeight = _a.virtualizedHeight, virtualizedLabelHeight = _a.virtualizedLabelHeight, onScroll = _a.onScroll, items = _a.items, itemSize = _a.itemSize, highlightedIndex = _a.highlightedIndex, inputValue = _a.inputValue, getItemProps = _a.getItemProps, maxHeight = _a.maxHeight;
    if (virtualizedHeight) {
        return (<react_virtualized_1.AutoSizer disableHeight>
        {function (_a) {
                var width = _a.width;
                return (<StyledList width={width} height={getHeight(items, maxHeight, virtualizedHeight, virtualizedLabelHeight)} onScroll={onScroll} rowCount={items.length} rowHeight={function (_a) {
                        var index = _a.index;
                        return items[index].groupLabel && virtualizedLabelHeight
                            ? virtualizedLabelHeight
                            : virtualizedHeight;
                    }} rowRenderer={function (_a) {
                        var key = _a.key, index = _a.index, style = _a.style;
                        return (<row_1.default key={key} item={items[index]} style={style} itemSize={itemSize} highlightedIndex={highlightedIndex} inputValue={inputValue} getItemProps={getItemProps}/>);
                    }}/>);
            }}
      </react_virtualized_1.AutoSizer>);
    }
    return (<React.Fragment>
      {items.map(function (item, index) { return (<row_1.default 
        // Using only the index of the row might not re-render properly,
        // because the items shift around the list
        key={item.value + "-" + index} item={item} itemSize={itemSize} highlightedIndex={highlightedIndex} inputValue={inputValue} getItemProps={getItemProps}/>); })}
    </React.Fragment>);
};
exports.default = List;
// XXX(ts): Emotion11 has some trouble with List's defaultProps
var StyledList = styled_1.default(react_virtualized_1.List)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  outline: none;\n"], ["\n  outline: none;\n"])));
var templateObject_1;
//# sourceMappingURL=list.jsx.map