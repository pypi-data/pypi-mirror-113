Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var memoize_1 = tslib_1.__importDefault(require("lodash/memoize"));
var getModalPortal = memoize_1.default(function () {
    var portal = document.getElementById('modal-portal');
    if (!portal) {
        portal = document.createElement('div');
        portal.setAttribute('id', 'modal-portal');
        document.body.appendChild(portal);
    }
    return portal;
});
exports.default = getModalPortal;
//# sourceMappingURL=getModalPortal.jsx.map