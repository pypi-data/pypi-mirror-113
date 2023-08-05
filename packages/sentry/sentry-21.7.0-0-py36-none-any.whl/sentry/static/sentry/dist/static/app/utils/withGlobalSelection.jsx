Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var globalSelectionStore_1 = tslib_1.__importDefault(require("app/stores/globalSelectionStore"));
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
/**
 * Higher order component that uses GlobalSelectionStore and provides the
 * active project
 */
function withGlobalSelection(WrappedComponent) {
    var WithGlobalSelection = /** @class */ (function (_super) {
        tslib_1.__extends(WithGlobalSelection, _super);
        function WithGlobalSelection() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = globalSelectionStore_1.default.get();
            _this.unsubscribe = globalSelectionStore_1.default.listen(function (selection) {
                if (_this.state !== selection) {
                    _this.setState(selection);
                }
            }, undefined);
            return _this;
        }
        WithGlobalSelection.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithGlobalSelection.prototype.render = function () {
            var _a = this.state, isReady = _a.isReady, selection = _a.selection;
            return (<WrappedComponent selection={selection} isGlobalSelectionReady={isReady} {...this.props}/>);
        };
        WithGlobalSelection.displayName = "withGlobalSelection(" + getDisplayName_1.default(WrappedComponent) + ")";
        return WithGlobalSelection;
    }(React.Component));
    return WithGlobalSelection;
}
exports.default = withGlobalSelection;
//# sourceMappingURL=withGlobalSelection.jsx.map