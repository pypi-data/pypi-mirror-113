Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var formSearch_1 = require("app/actionCreators/formSearch");
var formSearchStore_1 = tslib_1.__importDefault(require("app/stores/formSearchStore"));
var createFuzzySearch_1 = require("app/utils/createFuzzySearch");
var replaceRouterParams_1 = tslib_1.__importDefault(require("app/utils/replaceRouterParams"));
var FormSource = /** @class */ (function (_super) {
    tslib_1.__extends(FormSource, _super);
    function FormSource() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            fuzzy: null,
        };
        return _this;
    }
    FormSource.prototype.componentDidMount = function () {
        this.createSearch(this.props.searchMap);
    };
    FormSource.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.searchMap !== prevProps.searchMap) {
            this.createSearch(this.props.searchMap);
        }
    };
    FormSource.prototype.createSearch = function (searchMap) {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a;
            var _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.setState;
                        _b = {};
                        return [4 /*yield*/, createFuzzySearch_1.createFuzzySearch(searchMap || [], tslib_1.__assign(tslib_1.__assign({}, this.props.searchOptions), { keys: ['title', 'description'] }))];
                    case 1:
                        _a.apply(this, [(_b.fuzzy = _c.sent(),
                                _b)]);
                        return [2 /*return*/];
                }
            });
        });
    };
    FormSource.prototype.render = function () {
        var _a = this.props, searchMap = _a.searchMap, query = _a.query, params = _a.params, children = _a.children;
        var results = [];
        if (this.state.fuzzy) {
            var rawResults = this.state.fuzzy.search(query);
            results = rawResults.map(function (value) {
                var item = value.item, rest = tslib_1.__rest(value, ["item"]);
                return tslib_1.__assign({ item: tslib_1.__assign(tslib_1.__assign({}, item), { sourceType: 'field', resultType: 'field', to: replaceRouterParams_1.default(item.route, params) + "#" + encodeURIComponent(item.field.name) }) }, rest);
            });
        }
        return children({
            isLoading: searchMap === null,
            results: results,
        });
    };
    FormSource.defaultProps = {
        searchOptions: {},
    };
    return FormSource;
}(React.Component));
var FormSourceContainer = /** @class */ (function (_super) {
    tslib_1.__extends(FormSourceContainer, _super);
    function FormSourceContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            searchMap: formSearchStore_1.default.get(),
        };
        _this.unsubscribe = formSearchStore_1.default.listen(function (searchMap) { return _this.setState({ searchMap: searchMap }); }, undefined);
        return _this;
    }
    FormSourceContainer.prototype.componentDidMount = function () {
        // Loads form fields
        formSearch_1.loadSearchMap();
    };
    FormSourceContainer.prototype.componentWillUnmount = function () {
        this.unsubscribe();
    };
    FormSourceContainer.prototype.render = function () {
        return <FormSource searchMap={this.state.searchMap} {...this.props}/>;
    };
    return FormSourceContainer;
}(React.Component));
exports.default = react_router_1.withRouter(FormSourceContainer);
//# sourceMappingURL=formSource.jsx.map