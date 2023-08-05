Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var settingsBreadcrumbActions_1 = tslib_1.__importDefault(require("app/actions/settingsBreadcrumbActions"));
var BreadcrumbTitle = /** @class */ (function (_super) {
    tslib_1.__extends(BreadcrumbTitle, _super);
    function BreadcrumbTitle() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    BreadcrumbTitle.prototype.componentDidMount = function () {
        settingsBreadcrumbActions_1.default.mapTitle(this.props);
    };
    BreadcrumbTitle.prototype.render = function () {
        return null;
    };
    return BreadcrumbTitle;
}(react_1.Component));
exports.default = BreadcrumbTitle;
//# sourceMappingURL=breadcrumbTitle.jsx.map