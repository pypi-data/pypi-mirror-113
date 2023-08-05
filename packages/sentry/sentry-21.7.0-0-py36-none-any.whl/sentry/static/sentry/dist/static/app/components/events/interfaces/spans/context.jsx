Object.defineProperty(exports, "__esModule", { value: true });
exports.Consumer = exports.Provider = void 0;
var react_1 = require("react");
var SpanEntryContext = react_1.createContext({
    getViewChildTransactionTarget: function () { return undefined; },
});
exports.Provider = SpanEntryContext.Provider;
exports.Consumer = SpanEntryContext.Consumer;
//# sourceMappingURL=context.jsx.map