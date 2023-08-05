Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var tagStore_1 = tslib_1.__importDefault(require("app/stores/tagStore"));
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
/**
 * HOC for getting *only* tags from the TagStore.
 */
function withTags(WrappedComponent) {
    var WithTags = /** @class */ (function (_super) {
        tslib_1.__extends(WithTags, _super);
        function WithTags() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = {
                tags: tagStore_1.default.getAllTags(),
            };
            _this.unsubscribe = tagStore_1.default.listen(function (tags) { return _this.setState({ tags: tags }); }, undefined);
            return _this;
        }
        WithTags.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithTags.prototype.render = function () {
            var _a = this.props, tags = _a.tags, props = tslib_1.__rest(_a, ["tags"]);
            return <WrappedComponent {...tslib_1.__assign({ tags: tags !== null && tags !== void 0 ? tags : this.state.tags }, props)}/>;
        };
        WithTags.displayName = "withTags(" + getDisplayName_1.default(WrappedComponent) + ")";
        return WithTags;
    }(React.Component));
    return WithTags;
}
exports.default = withTags;
//# sourceMappingURL=withTags.jsx.map