Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var isNil_1 = tslib_1.__importDefault(require("lodash/isNil"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
/**
 * Retrieves metadata from an object (object should be a proxy that
 * has been decorated using `app/components/events/meta/metaProxy/withMeta`
 */
var MetaData = function (_a) {
    var children = _a.children, object = _a.object, prop = _a.prop, required = _a.required;
    var value = object[prop];
    var meta = metaProxy_1.getMeta(object, prop);
    if (required && isNil_1.default(value) && !meta) {
        return null;
    }
    return <errorBoundary_1.default mini>{children(value, meta)}</errorBoundary_1.default>;
};
exports.default = MetaData;
//# sourceMappingURL=metaData.jsx.map