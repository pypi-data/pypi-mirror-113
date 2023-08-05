Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var MOCK_ORG = TestStubs.Organization();
var DEFAULTS = {
    organization: MOCK_ORG,
    organizations: [MOCK_ORG],
    project: TestStubs.Project(),
    lastRoute: {},
};
var withLatestContextMock = function (WrappedComponent) {
    return /** @class */ (function (_super) {
        tslib_1.__extends(WithLatestContextMockWrapper, _super);
        function WithLatestContextMockWrapper() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        WithLatestContextMockWrapper.prototype.render = function () {
            return <WrappedComponent {...DEFAULTS} {...this.props}/>;
        };
        return WithLatestContextMockWrapper;
    }(react_1.Component));
};
exports.default = withLatestContextMock;
//# sourceMappingURL=withLatestContext.jsx.map