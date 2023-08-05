Object.defineProperty(exports, "__esModule", { value: true });
exports.isWithinToken = exports.getKeyName = exports.treeTransformer = exports.treeResultLocator = void 0;
var tslib_1 = require("tslib");
var parser_1 = require("./parser");
/**
 * Used internally within treeResultLocator to stop recursion once we've
 * located a matched result.
 */
var TokenResultFound = /** @class */ (function (_super) {
    tslib_1.__extends(TokenResultFound, _super);
    function TokenResultFound(result) {
        var _this = _super.call(this) || this;
        _this.result = result;
        return _this;
    }
    return TokenResultFound;
}(Error));
/**
 * Used as the marker to skip token traversal in treeResultLocator
 */
var skipTokenMarker = Symbol('Returned to skip visiting a token');
/**
 * Utility function to visit every Token node within an AST tree (in DFS order)
 * and apply a test method that may choose to return some value from that node.
 *
 * You must call the `returnValue` method for a result to be returned.
 *
 * When returnValue is never called and all nodes of the search tree have been
 * visited the noResultValue will be returned.
 */
function treeResultLocator(_a) {
    var tree = _a.tree, visitorTest = _a.visitorTest, noResultValue = _a.noResultValue;
    var returnResult = function (result) { return new TokenResultFound(result); };
    var nodeVisitor = function (token) {
        var result = visitorTest({ token: token, returnResult: returnResult, skipToken: skipTokenMarker });
        // Bubble the result back up.
        //
        // XXX: Using a throw here is a bit easier than threading the return value
        // back up through the recursive call tree.
        if (result instanceof TokenResultFound) {
            throw result;
        }
        // Don't traverse into any nested tokens
        if (result === skipTokenMarker) {
            return;
        }
        switch (token.type) {
            case parser_1.Token.Filter:
                nodeVisitor(token.key);
                nodeVisitor(token.value);
                break;
            case parser_1.Token.KeyExplicitTag:
                nodeVisitor(token.key);
                break;
            case parser_1.Token.KeyAggregate:
                nodeVisitor(token.name);
                token.args && nodeVisitor(token.args);
                nodeVisitor(token.argsSpaceBefore);
                nodeVisitor(token.argsSpaceAfter);
                break;
            case parser_1.Token.LogicGroup:
                token.inner.forEach(nodeVisitor);
                break;
            case parser_1.Token.KeyAggregateArgs:
                token.args.forEach(function (v) { return nodeVisitor(v.value); });
                break;
            case parser_1.Token.ValueNumberList:
            case parser_1.Token.ValueTextList:
                token.items.forEach(function (v) { return nodeVisitor(v.value); });
                break;
            default:
        }
    };
    try {
        tree.forEach(nodeVisitor);
    }
    catch (error) {
        if (error instanceof TokenResultFound) {
            return error.result;
        }
        throw error;
    }
    return noResultValue;
}
exports.treeResultLocator = treeResultLocator;
/**
 * Utility function to visit every Token node within an AST tree and apply
 * a transform to those nodes.
 */
function treeTransformer(_a) {
    var tree = _a.tree, transform = _a.transform;
    var nodeVisitor = function (token) {
        switch (token.type) {
            case parser_1.Token.Filter:
                return transform(tslib_1.__assign(tslib_1.__assign({}, token), { key: nodeVisitor(token.key), value: nodeVisitor(token.value) }));
            case parser_1.Token.KeyExplicitTag:
                return transform(tslib_1.__assign(tslib_1.__assign({}, token), { key: nodeVisitor(token.key) }));
            case parser_1.Token.KeyAggregate:
                return transform(tslib_1.__assign(tslib_1.__assign({}, token), { name: nodeVisitor(token.name), args: token.args ? nodeVisitor(token.args) : token.args, argsSpaceBefore: nodeVisitor(token.argsSpaceBefore), argsSpaceAfter: nodeVisitor(token.argsSpaceAfter) }));
            case parser_1.Token.LogicGroup:
                return transform(tslib_1.__assign(tslib_1.__assign({}, token), { inner: token.inner.map(nodeVisitor) }));
            case parser_1.Token.KeyAggregateArgs:
                return transform(tslib_1.__assign(tslib_1.__assign({}, token), { args: token.args.map(function (v) { return (tslib_1.__assign(tslib_1.__assign({}, v), { value: nodeVisitor(v.value) })); }) }));
            case parser_1.Token.ValueNumberList:
            case parser_1.Token.ValueTextList:
                return transform(tslib_1.__assign(tslib_1.__assign({}, token), { 
                    // TODO(ts): Not sure why `v` cannot be inferred here
                    items: token.items.map(function (v) { return (tslib_1.__assign(tslib_1.__assign({}, v), { value: nodeVisitor(v.value) })); }) }));
            default:
                return transform(token);
        }
    };
    return tree.map(nodeVisitor);
}
exports.treeTransformer = treeTransformer;
/**
 * Utility to get the string name of any type of key.
 */
var getKeyName = function (key, options) {
    if (options === void 0) { options = {}; }
    var aggregateWithArgs = options.aggregateWithArgs;
    switch (key.type) {
        case parser_1.Token.KeySimple:
            return key.value;
        case parser_1.Token.KeyExplicitTag:
            return key.key.value;
        case parser_1.Token.KeyAggregate:
            return aggregateWithArgs
                ? key.name.value + "(" + (key.args ? key.args.text : '') + ")"
                : key.name.value;
        default:
            return '';
    }
};
exports.getKeyName = getKeyName;
function isWithinToken(node, position) {
    return position >= node.location.start.offset && position <= node.location.end.offset;
}
exports.isWithinToken = isWithinToken;
//# sourceMappingURL=utils.jsx.map