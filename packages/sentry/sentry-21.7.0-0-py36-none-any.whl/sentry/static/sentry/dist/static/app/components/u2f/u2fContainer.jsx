Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var u2fsign_1 = tslib_1.__importDefault(require("./u2fsign"));
var U2fContainer = /** @class */ (function (_super) {
    tslib_1.__extends(U2fContainer, _super);
    function U2fContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            authenticators: [],
        };
        return _this;
    }
    U2fContainer.prototype.componentDidMount = function () {
        this.getAuthenticators();
    };
    U2fContainer.prototype.getAuthenticators = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var api, authenticators, _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        api = this.props.api;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise('/authenticators/')];
                    case 2:
                        authenticators = _b.sent();
                        this.setState({ authenticators: authenticators !== null && authenticators !== void 0 ? authenticators : [] });
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    U2fContainer.prototype.render = function () {
        var _this = this;
        var className = this.props.className;
        var authenticators = this.state.authenticators;
        if (!authenticators.length) {
            return null;
        }
        return (<div className={className}>
        {authenticators.map(function (auth) {
                return auth.id === 'u2f' && auth.challenge ? (<u2fsign_1.default key={auth.id} {..._this.props} challengeData={auth.challenge}/>) : null;
            })}
      </div>);
    };
    return U2fContainer;
}(react_1.Component));
exports.default = withApi_1.default(U2fContainer);
//# sourceMappingURL=u2fContainer.jsx.map