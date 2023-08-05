Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var SidebarMenuItemLink = function (_a) {
    var to = _a.to, href = _a.href, props = tslib_1.__rest(_a, ["to", "href"]);
    if (href) {
        return <externalLink_1.default href={href} {...props}/>;
    }
    if (to) {
        return <link_1.default to={to} {...props}/>;
    }
    return <div tabIndex={0} {...props}/>;
};
exports.default = SidebarMenuItemLink;
//# sourceMappingURL=sidebarMenuItemLink.jsx.map